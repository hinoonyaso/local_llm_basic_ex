# text to image : mac에서만 지원함, 2026.08.04 기준

# x/z-image-turbo   Alibaba Tongyi Lab의 6B text-to-image 모델
# x/flux2-klein   Black Forest Labs 계열 이미지 생성 모델, 4B/9B 제공

# import subprocess
# from pathlib import Path
# from datetime import datetime


# MODEL_NAME = "x/flux2-klein"
# OUTPUT_DIR = Path("img_output")


# def get_image_files(directory: Path) -> set[Path]:
#     """디렉터리 안의 이미지 파일 목록을 반환한다."""
#     image_extensions = {".png", ".jpg", ".jpeg", ".webp"}
#     return {
#         path
#         for path in directory.iterdir()
#         if path.is_file() and path.suffix.lower() in image_extensions
#     }


# def generate_image_with_ollama(
#     prompt: str,
#     model: str = MODEL_NAME,
#     output_dir: Path = OUTPUT_DIR,
# ) -> Path | None:
#     """
#     Ollama의 x/flux2-klein 모델로 이미지를 생성한다.

#     Ollama 이미지 생성 모델은 결과 이미지를 현재 작업 디렉터리에 저장한다.
#     따라서 output_dir로 이동한 뒤 ollama run 명령을 실행하고,
#     생성 전후 파일 목록을 비교해 새 이미지 파일을 찾는다.
#     """

#     output_dir.mkdir(parents=True, exist_ok=True)

#     before_files = get_image_files(output_dir)

#     command = [
#         "ollama",
#         "run",
#         model,
#         prompt,
#     ]

#     print("이미지 생성 요청 중...")
#     print("모델:", model)
#     print("프롬프트:", prompt)

#     try:
#         result = subprocess.run(
#             command,
#             cwd=output_dir,
#             text=True,
#             capture_output=True,
#             check=True,
#         )

#         if result.stdout:
#             print("\n[Ollama 출력]")
#             print(result.stdout)

#         if result.stderr:
#             print("\n[Ollama 경고/로그]")
#             print(result.stderr)

#     except FileNotFoundError:
#         print("오류: ollama 명령을 찾을 수 없다. Ollama 설치 여부와 PATH 설정을 확인해야 한다.")
#         return None

#     except subprocess.CalledProcessError as e:
#         print("오류: 이미지 생성 명령 실행에 실패했다.")
#         print("\n[stdout]")
#         print(e.stdout)
#         print("\n[stderr]")
#         print(e.stderr)
#         return None

#     after_files = get_image_files(output_dir)
#     new_files = after_files - before_files

#     if not new_files:
#         print("새로 생성된 이미지 파일을 찾지 못했다.")
#         print("현재 OS에서 Ollama 이미지 생성이 지원되지 않거나, 이미지 저장 방식이 달라졌을 수 있다.")
#         return None

#     latest_image = max(new_files, key=lambda path: path.stat().st_mtime)

#     print("\n이미지 생성 완료:")
#     print(latest_image)

#     return latest_image


# if __name__ == "__main__":
#     prompt = (
#         "A clean modern todo app landing page, "
#         "soft green background, minimal UI, "
#         "readable text saying 'TODO APP', "
#         "flat design, high quality, 1024x1024"
#     )

#     generated_path = generate_image_with_ollama(prompt)

#     if generated_path:
#         print("\n저장 위치:", generated_path.resolve())

import torch
from pathlib import Path
from datetime import datetime
from diffusers import AutoPipelineForText2Image


MODEL_NAME = "stabilityai/sdxl-turbo"
OUTPUT_DIR = Path("img_output")


def load_pipeline(model: str = MODEL_NAME):
    """diffusers 파이프라인을 로드하고 사용 가능한 경우 GPU로 옮긴다."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    pipeline = AutoPipelineForText2Image.from_pretrained(
        model,
        torch_dtype=dtype,
        variant="fp16" if device == "cuda" else None,
    )
    pipeline = pipeline.to(device)

    return pipeline


def generate_image(
    prompt: str,
    pipeline=None,
    model: str = MODEL_NAME,
    output_dir: Path = OUTPUT_DIR,
) -> Path | None:
    """sdxl-turbo로 이미지를 생성하고 output_dir에 저장한다."""

    output_dir.mkdir(parents=True, exist_ok=True)

    print("이미지 생성 요청 중...")
    print("모델:", model)
    print("프롬프트:", prompt)

    if pipeline is None:
        pipeline = load_pipeline(model)

    # sdxl-turbo는 guidance_scale=0.0, 1~4 step으로 빠르게 생성하도록 설계됨
    result = pipeline(
        prompt=prompt,
        num_inference_steps=2,
        guidance_scale=0.0,
    )
    image = result.images[0]

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = output_dir / f"image_{timestamp}.png"
    image.save(output_path)

    print("\n이미지 생성 완료:")
    print(output_path)

    return output_path


if __name__ == "__main__":
    prompt = """
Please draw a funny stray orange tabby cat doing a one-arm handstand.

The cat is an orange-and-white street cat with a slightly scruffy look, like a typical cheese-colored stray cat.
It is balancing upside down on only one front paw, while the other three legs are awkwardly stretched in different directions.

The cat has an extremely serious and confident facial expression, as if it is performing an amazing professional stunt.
Make the contrast between the ridiculous pose and the serious face very funny.

Show the full body clearly.
Add a simple Korean alley or street background to make it feel like a real stray cat suddenly showing off an absurd acrobatic trick.

Comedic illustration style, exaggerated dynamic pose, expressive face, detailed orange tabby fur, high quality, 1024x1024.

"""
    generated_path = generate_image(prompt)

    if generated_path:
        print("\n저장 위치:", generated_path.resolve())