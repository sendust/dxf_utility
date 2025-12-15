import ezdxf
import os

def load_dxf(path: str):
    return ezdxf.readfile(path)


def get_layers(doc):
    # 모든 layer 이름 목록 (순서 유지)
    return [layer.dxf.name for layer in doc.layers]


def count_entities_in_layer(doc, layer_name: str) -> int:
    cnt = 0
    for e in doc.entitydb.values():
        try:
            if e.dxf.layer == layer_name:
                cnt += 1
        except Exception:
            pass
    return cnt


def print_layers(doc, deleted_layers: set):
    print("\n현재 Layer 목록")
    print("번호 | Layer 이름 | Entity 개수")
    print("--------------------------------")

    index_map = {}
    idx = 1
    for layer_name in get_layers(doc):
        if layer_name in deleted_layers:
            continue
        cnt = count_entities_in_layer(doc, layer_name)
        print(f"{idx:>4} | {layer_name:<10} | {cnt}")
        index_map[idx] = layer_name
        idx += 1

    return index_map


def delete_layer_entities(doc, layer_name: str):
    # 해당 layer 의 모든 entity 삭제
    to_delete = []
    for e in doc.entitydb.values():
        try:
            if e.dxf.layer == layer_name:
                to_delete.append(e)
        except Exception:
            pass

    for e in to_delete:
        doc.entitydb.delete_entity(e)


def main():
    path = input("DXF 파일 경로를 입력하세요: ").strip('"')
    if not os.path.exists(path):
        print("파일이 존재하지 않습니다")
        return

    doc = load_dxf(path)
    deleted_layers = set()

    index_map = print_layers(doc, deleted_layers)

    while True:
        cmd = input("\n삭제할 layer 번호 / save / list / quit : ").strip().lower()

        if cmd == 'quit':
            print("종료합니다")
            break

        elif cmd == 'list':
            index_map = print_layers(doc, deleted_layers)

        elif cmd == 'save':
            base, ext = os.path.splitext(path)
            new_path = base + '_layer' + ext
            doc.saveas(new_path)
            print(f"저장 완료: {new_path}")

        elif cmd.isdigit():
            num = int(cmd)
            if num not in index_map:
                print("잘못된 번호입니다")
                continue

            layer_name = index_map[num]
            delete_layer_entities(doc, layer_name)
            deleted_layers.add(layer_name)
            print(f"Layer '{layer_name}' 의 모든 entity 를 삭제했습니다")

        else:
            print("알 수 없는 명령입니다")


if __name__ == '__main__':
    main()
