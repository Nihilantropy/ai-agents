import torch

print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    # Get first GPU properties
    gpu_props = torch.cuda.get_device_properties(0)
    
    print(f"\nGPU Name: {gpu_props.name}")
    print(f"Total Memory: {gpu_props.total_memory/1e9:.2f} GB")
    print(f"CUDA Runtime Version: {torch.version.cuda}")
    print(f"Compute Capability: {gpu_props.major}.{gpu_props.minor}")
    print(f"PyTorch CUDA Arch List: {torch.cuda.get_arch_list()}")
else:
    print("No CUDA-capable device detected")