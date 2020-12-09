from __future__ import annotations
from typing import Optional

class Instruction:

    read_operands: list[str]
    write_operands: list[str]

    def __init__(self, read_operands: list[str], write_operands: list[str]) -> None:
        self.read_operands = read_operands
        self.write_operands = write_operands


class Block:

    live_use: set
    live_def: set
    live_out: set
    live_in: set
    instructions: list[Instruction]
    successors: Optional[list[Block]]

    def __init__(self, instructions: list[Instruction], successors: Optional[list[Block]]=None) -> None:
        self.instructions = instructions
        self.live_in = set()
        self.live_out = set()
        self.successors = successors

class ControlFlow:

    blocks: list[Block]

    def __init__(self, blocks: list[Block]):
        self.blocks = blocks


def solve_live_use_live_def(g: ControlFlow) -> ControlFlow:
    for block in g.blocks:
        block.live_use = set()
        block.live_def = set()
        for instriction in block.instructions:
            for v in instriction.read_operands:
                if v not in block.live_def:
                    block.live_use.add(v)
                
            for v in instriction.write_operands:
                block.live_def.add(v)
    return g


def solve_live_in_live_out(g: ControlFlow) -> ControlFlow:
    iters = 1
    has_block_changed = True
    while has_block_changed:
        print(f"{iters} iteration(s)")
        i = 1
        block_live_out = []
        for block in reversed(g.blocks):
            temp_live_out = block.live_out
            for successor in block.successors:
                block.live_out = block.live_out.union(successor.live_in)
            block_live_out.append(block.live_out != temp_live_out)
            block.live_in = block.live_out.difference(block.live_def).union(block.live_use)
            print(f"\tblock {len(g.blocks)-i}\n\t\tliveIn: {block.live_in}\n\t\tliveOut: {block.live_out}")
            i+=1
        iters +=1
        has_block_changed = any(live_out for live_out in block_live_out)
    return g




def main():
    blocks = [
        Block([]),
        Block([
            Instruction(read_operands=[], write_operands=["v32"]),
            Instruction(read_operands=["a0"], write_operands=["v33"]),
            Instruction(read_operands=["v32"], write_operands=["v34"])
        ]),
        Block([
            Instruction(read_operands=[], write_operands=["v35"]),
            Instruction(read_operands=["v33"], write_operands=["v35"])
        ]),
        Block([
            Instruction(read_operands=[], write_operands=["v36"]),
            Instruction(read_operands=["v33", "v36"], write_operands=["v37"]),
            Instruction(read_operands=["v33", "v34"], write_operands=["v38"]),
            Instruction(read_operands=["v38"], write_operands=["v34"]),
            Instruction(read_operands=["v37"], write_operands=["v33"]),
        ]),
        Block([
            Instruction(read_operands=["v34"], write_operands=["v0"]),
            Instruction(read_operands=["v0"], write_operands=[])
        ])
    ]
    blocks[0].successors = [blocks[1]]
    blocks[1].successors = [blocks[2]]
    blocks[2].successors = [blocks[3], blocks[4]]
    blocks[3].successors = [blocks[2]]
    blocks[4].successors = []

    control_flow = ControlFlow(blocks)
    control_flow = solve_live_use_live_def(g=control_flow)
    i = 0
    for block in control_flow.blocks:
        print(f"block {i}:\n\tliveUse: {block.live_use}\n\tliveDef: {block.live_def}")
        i+= 1
    
    control_flow = solve_live_in_live_out(g=control_flow)
        



if __name__ == "__main__":
    main()