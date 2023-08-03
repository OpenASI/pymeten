import torch
import triton
import triton.language as tl

from pymeten import triton_benchmark_sizes, MetricUnit, MetricConfig

def test_triton_add():
    if not torch.cuda.is_available():
        return

    @triton.jit
    def add_kernel(
        x_ptr,  # *Pointer* to first input vector.
        y_ptr,  # *Pointer* to second input vector.
        output_ptr,  # *Pointer* to output vector.
        n_elements,  # Size of the vector.
        BLOCK_SIZE: tl.constexpr,
    ):
        pid = tl.program_id(axis=0)  # We use a 1D launch grid so axis is 0. 0, 1, or 2
        block_start = pid * BLOCK_SIZE
        offsets = block_start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < n_elements
        x = tl.load(x_ptr + offsets, mask=mask)
        y = tl.load(y_ptr + offsets, mask=mask)
        output = x + y
        tl.store(output_ptr + offsets, output, mask=mask)


    def add(x: torch.Tensor, y: torch.Tensor):
        output = torch.empty_like(x)
        assert x.is_cuda and y.is_cuda and output.is_cuda
        n_elements = output.numel()
        grid = lambda meta: (triton.cdiv(n_elements, meta['BLOCK_SIZE']),)
        add_kernel[grid](x, y, output, n_elements, BLOCK_SIZE=1024)
        return output


    inputs = {
        'x': lambda size: torch.rand(size, device='cuda', dtype=torch.float32),
        'y': lambda size: torch.rand(size, device='cuda', dtype=torch.float32)
    }

    kernels = {
        'torch': lambda x, y: x+y,
        'triton': lambda x, y : add(x, y)
    }

    triton_benchmark_sizes(inputs, kernels, sizes=[2**i for i in range(12, 13)],
                        metric_config=MetricConfig(
                            MetricUnit.GBPS,
                            num_bytes=12))
