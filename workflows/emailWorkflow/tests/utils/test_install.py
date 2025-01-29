import torch
from ollama import Client
import sys

def test_gpu():
    try:
        assert torch.cuda.is_available(), "CUDA not available"
        device_count = torch.cuda.device_count()
        assert device_count > 0, f"No GPU detected (found {device_count} devices)"
        
        gpu_props = torch.cuda.get_device_properties(0)
        print(f"[✓] GPU: {gpu_props.name}")
        print(f"    VRAM: {gpu_props.total_memory/1e9:.2f} GB")
        print(f"    Compute Capability: {gpu_props.major}.{gpu_props.minor}")
        return True
    except Exception as e:
        print(f"[×] GPU Test Failed: {str(e)}")
        return False

def test_torch_cuda():
    try:
        x = torch.randn(3, 3).cuda()
        y = torch.randn(3, 3).cuda()
        z = (x + y).sum()
        assert not torch.isnan(z), "CUDA operation produced NaN"
        print("[✓] PyTorch CUDA operations validated")
        return True
    except Exception as e:
        print(f"[×] CUDA Operations Failed: {str(e)}")
        return False

def test_ollama_connection():
    client = Client()
    try:
        # Official API check from docs
        response = client.list()
        assert 'models' in response, "Invalid server response"
        print("[✓] Ollama server is reachable")
        
        # Model existence check
        target_model = 'deepseek-r1:32b'
        models = [model['model'] for model in response['models']]
        assert any(target_model == model for model in models), (
            f"Model '{target_model}' not found. Available models: {', '.join(models)}"
        )
        print(f"[✓] Model '{target_model}' is available")
        return True
    except Exception as e:
        print(f"[×] Ollama Connection Failed: {str(e)}")
        return False

def main():
    print("Running System Checks:\n" + "-"*40)
    
    results = {
        "gpu": test_gpu(),
        "cuda_ops": test_torch_cuda(),
        "ollama": test_ollama_connection()
    }
    
    print("\nSummary:")
    for test, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{test.upper():<10} {status}")
    
    if all(results.values()):
        print("\nSystem is ready for AI workflows!")
        sys.exit(0)
    else:
        print("\nSome checks failed. See above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()