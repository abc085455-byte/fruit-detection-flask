from huggingface_hub import hf_hub_download

# model ko download karo locally
model_path = hf_hub_download(repo_id="aiarenm/yolo_finetuned_fruits", filename="best.pt")
print(model_path)
