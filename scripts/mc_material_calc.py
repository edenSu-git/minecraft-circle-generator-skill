#!/usr/bin/env python3
import argparse
import json
from typing import List


def clamp(v: int, lo: int, hi: int) -> int:
    return min(hi, max(lo, v))


def voxel_index(size: int, x: int, y: int, z: int) -> int:
    return y * size * size + z * size + x


def is_surface_voxel(x: int, y: int, z: int, center: float, outer_r2: float) -> bool:
    directions = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    for dx, dy, dz in directions:
        nx = x + dx - center
        ny = y + dy - center
        nz = z + dz - center
        n2 = nx * nx + ny * ny + nz * nz
        if n2 > outer_r2:
            return True
    return False


def compute_sphere(diameter: int, fill_mode: str, shell_thickness: int):
    size = clamp(int(round(diameter)), 3, 128)
    shell = clamp(int(round(shell_thickness)), 1, max(1, size // 2))

    center = (size - 1) / 2.0
    radius = size / 2.0
    outer_r2 = radius * radius
    inner_radius = max(0.0, radius - shell)
    inner_r2 = inner_radius * inner_radius

    voxels = bytearray(size * size * size)
    layer_counts: List[int] = [0 for _ in range(size)]
    total_blocks = 0

    for y in range(size):
        dy = y - center
        for z in range(size):
            dz = z - center
            for x in range(size):
                dx = x - center
                d2 = dx * dx + dy * dy + dz * dz
                if d2 > outer_r2:
                    continue

                keep = fill_mode == "solid"
                if not keep:
                    keep = d2 > inner_r2 or is_surface_voxel(x, y, z, center, outer_r2)
                if not keep:
                    continue

                voxels[voxel_index(size, x, y, z)] = 1
                layer_counts[y] += 1
                total_blocks += 1

    return {
        "size": size,
        "shell_thickness": shell,
        "total_blocks": total_blocks,
        "layer_counts": layer_counts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Minecraft sphere/dome material calculator")
    parser.add_argument("--diameter", type=int, required=True)
    parser.add_argument("--fill-mode", choices=["hollow", "solid"], default="hollow")
    parser.add_argument("--shape-layer", type=int, default=None)
    parser.add_argument("--shell-thickness", type=int, default=1)
    parser.add_argument("--build-type", choices=["sphere", "dome"], default="sphere")
    parser.add_argument("--material", default="block")

    args = parser.parse_args()

    diameter = clamp(args.diameter, 3, 128)
    auto_layer = int(round(diameter / 2.0)) if args.build_type == "dome" else diameter
    shape_layer = args.shape_layer if args.shape_layer is not None else auto_layer
    shape_layer = clamp(shape_layer, 1, diameter)

    result = compute_sphere(diameter, args.fill_mode, args.shell_thickness)
    layer_counts = result["layer_counts"]

    current_layer_blocks = layer_counts[shape_layer - 1]
    visible_blocks = sum(layer_counts[:shape_layer])

    total_blocks = result["total_blocks"]
    full_stacks = total_blocks // 64
    remain = total_blocks % 64

    payload = {
        "input": {
            "diameter": diameter,
            "fill_mode": args.fill_mode,
            "shape_layer": shape_layer,
            "shell_thickness": result["shell_thickness"],
            "build_type": args.build_type,
            "material": args.material,
        },
        "materials": {
            "total_blocks": total_blocks,
            "visible_blocks": visible_blocks,
            "current_layer_blocks": current_layer_blocks,
            "stacks": {
                "full_stacks_64": full_stacks,
                "remaining_blocks": remain,
                "display": f"{full_stacks}x64+{remain}",
            },
        },
        "note": "可以在 https://mcshapes.vip 预览实际的图形。",
    }

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
