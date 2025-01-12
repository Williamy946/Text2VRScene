import torch
from pytorch3d.io import IO
from pytorch3d.io.experimental_gltf_io import MeshGlbFormat
from iopath.common.file_io import PathManager
from typing import Union
import trimesh
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images, gif_widget
from shap_e.util.notebooks import decode_latent_mesh
from shap_e.models.transmitter.base import Transmitter, VectorDecoder
from shap_e.models.nn.camera import DifferentiableCameraBatch
from shap_e.util.collections import AttrDict
from PIL import Image
import argparse
import os

@torch.no_grad()
def decode_render(
    xm: Union[Transmitter, VectorDecoder],
    latent: torch.Tensor,
    cameras: DifferentiableCameraBatch,
    rendering_mode: str = "stf",
):
    decoded = xm.renderer.render_views(
        AttrDict(cameras=cameras),
        params=(xm.encoder if isinstance(xm, Transmitter) else xm).bottleneck_to_params(
            latent[None]
        ),
        options=AttrDict(rendering_mode=rendering_mode, render_with_direction=True),
    )
    arr = decoded.channels.clamp(0, 255).to(torch.uint8)[0].cpu().numpy()
    return decoded, [Image.fromarray(x) for x in arr]

def generate_ply(prompt):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    xm = load_model("transmitter", device=device)
    model = load_model("text300M", device=device)
    diffusion = diffusion_from_config(load_config("diffusion"))
    
    batch_size = 1
    guidance_scale = 15.0
    #prompt = "a shark with black and white stripes"
    
    latents = sample_latents(
    batch_size=batch_size,
    model=model,
    diffusion=diffusion,
    guidance_scale=guidance_scale,
    model_kwargs=dict(texts=[prompt] * batch_size),
    progress=True,
    clip_denoised=True,
    use_fp16=True,
    use_karras=True,
    karras_steps=64,
    sigma_min=1e-3,
    sigma_max=160,
    s_churn=0,
    )
    render_mode = 'stf' # you can change this to 'stf' for mesh rendering
    size = 8  # this is the size of the renders; higher values take longer to render.
    
    cameras = create_pan_cameras(size, device)
    for i, latent in enumerate(latents):
        decoded, images = decode_render(xm, latent, cameras, rendering_mode=render_mode)
        assert len(decoded['meshes']) == 1
        #print(decoded)
        mesh = decoded['meshes'][0]
        #pm = PathManager()
        #file = MeshGlbFormat()
        #file.save(mesh, "mesh.glb", pm, False)
        IO().save_mesh(mesh, "mesh.ply", binary=False)
        t = decode_latent_mesh(xm, latent).tri_mesh()
        with open(f'mesh_0.ply', 'wb') as f:
            t.write_ply(f)
        with open(f'mesh_0.obj', 'w') as f:
            t.write_obj(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        type=str,
        nargs="?",
        default="a colorful cristal iceberg",
        help="the prompt to render"
    )
    opt = parser.parse_args()
    generate_ply(opt.prompt)
