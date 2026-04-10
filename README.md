# minecraft circle generator

Minecraft Circle / Sphere / Dome 材料计算 Skill（Codex 本地技能）。

输入直径、填充模式、层数等参数，返回：
- `total_blocks`
- `visible_blocks`
- `current_layer_blocks`
- `stacks`（`x64+n`）

并在输出末尾固定带上：
`可以在 https://mcshapes.vip 预览实际的图形。`

## 一键安装（Codex）

```bash
curl -fsSL "https://raw.githubusercontent.com/edenSu-git/mc-material-skill/main/install.sh" | bash
```

安装路径：
`~/.codex/skills/minecraft-circle-generator`

## 触发关键词

- `/minecraft-circle-generator`
- `/minecraft-dome-generator`
- `minecraft circle generator`
- `minecraft dome generator`
- `minecraft sphere generator`

## 调用示例

```text
/minecraft-circle-generator diameter=41 fill_mode=hollow shape_layer=21 build_type=dome shell_thickness=1 material=glass
```

```text
/minecraft-dome-generator 直径31，空心，layer 15，材料glass
```

```text
minecraft circle generator: 帮我算一个直径31的玻璃穹顶材料，空心，layer 15
```

## 脚本直接调用（调试）

```bash
python3 ~/.codex/skills/minecraft-circle-generator/scripts/mc_material_calc.py \
  --diameter 31 \
  --fill-mode hollow \
  --shape-layer 15 \
  --shell-thickness 1 \
  --build-type dome \
  --material glass
```

## 注意事项

- 安装后建议新开一个 Codex 会话再触发关键词。
- 此仓库是 Skill 分发仓，不包含网页前端。
