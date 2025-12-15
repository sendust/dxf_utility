import ezdxf
import os

def load_dxf(path: str):
    return ezdxf.readfile(path)


def get_blocks(doc):
    # 익명 블록(*U, *D 등) 제외, 실제 정의된 block만 대상
    blocks = []
    for blk in doc.blocks:
        name = blk.name
        if not name.startswith('*'):  # anonymous block 제외
            blocks.append(name)
    return blocks


def count_block_inserts(doc, block_name: str) -> int:
    cnt = 0
    for e in doc.entitydb.values():
        try:
            if e.dxftype() == 'INSERT' and e.dxf.name == block_name:
                cnt += 1
        except Exception:
            pass
    return cnt


def print_blocks(doc, deleted_blocks: set):
    print("\n현재 Block 목록")
    print("번호 | Block 이름 | 사용 개수")
    print("--------------------------------")

    index_map = {}
    idx = 1
    for name in get_blocks(doc):
        if name in deleted_blocks:
            continue
        cnt = count_block_inserts(doc, name)
        print(f"{idx:>4} | {name:<12} | {cnt}")
        index_map[idx] = name
        idx += 1

    return index_map


def delete_block(doc, block_name: str):
    # 1) 도면에 사용된 INSERT 제거
    to_delete = []
    for e in doc.entitydb.values():
        try:
            if e.dxftype() == 'INSERT' and e.dxf.name == block_name:
                to_delete.append(e)
        except Exception:
            pass

    for e in to_delete:
        doc.entitydb.delete_entity(e)

    # 2) block 정의 삭제
    if block_name in doc.blocks:
        doc.blocks.delete_block(block_name, safe=False)


def main():
    path = input("DXF 파일 경로를 입력하세요: ").strip('"')
    if not os.path.exists(path):
        print("파일이 존재하지 않습니다")
        return

    doc = load_dxf(path)
    deleted_blocks = set()

    index_map = print_blocks(doc, deleted_blocks)

    while True:
        cmd = input("\n삭제할 block 번호 / save / list / quit : ").strip().lower()

        if cmd == 'quit':
            print("종료합니다")
            break

        elif cmd == 'list':
            index_map = print_blocks(doc, deleted_blocks)

        elif cmd == 'save':
            base, ext = os.path.splitext(path)
            new_path = base + '_block' + ext
            doc.saveas(new_path)
            print(f"저장 완료: {new_path}")

        elif cmd.isdigit():
            num = int(cmd)
            if num not in index_map:
                print("잘못된 번호입니다")
                continue

            block_name = index_map[num]
            delete_block(doc, block_name)
            deleted_blocks.add(block_name)
            print(f"Block '{block_name}' 이(가) 도면에서 제거되고 정의도 삭제되었습니다")

        else:
            print("알 수 없는 명령입니다")


if __name__ == '__main__':
    main()
