import ezdxf
import os

def load_dxf(path: str):
    return ezdxf.readfile(path)


def get_styles(doc):
    # TEXT STYLE 목록
    return list(doc.styles)


def count_text_using_style(doc, style_name: str) -> int:
    cnt = 0
    for e in doc.entitydb.values():
        try:
            if e.dxftype() in ('TEXT', 'MTEXT') and e.dxf.style == style_name:
                cnt += 1
        except Exception:
            pass
    return cnt


def print_fonts(doc):
    print("\n현재 Font 목록 (STYLE 기준)")
    print("번호 | Style 이름 | Font 파일 | 사용 개수")
    print("------------------------------------------------")

    index_map = {}
    idx = 1
    for style in get_styles(doc):
        name = style.dxf.name
        font = style.dxf.font
        cnt = count_text_using_style(doc, name)
        print(f"{idx:>4} | {name:<10} | {font:<12} | {cnt}")
        index_map[idx] = style
        idx += 1

    return index_map


def replace_font(style, new_font: str):
    style.dxf.font = new_font


def main():
    path = input("DXF 파일 경로를 입력하세요: ").strip('"')
    if not os.path.exists(path):
        print("파일이 존재하지 않습니다")
        return

    doc = load_dxf(path)

    index_map = print_fonts(doc)

    while True:
        cmd = input("\n번호 입력 / save / list / quit : ").strip().lower()

        if cmd == 'quit':
            print("종료합니다")
            break

        elif cmd == 'list':
            index_map = print_fonts(doc)

        elif cmd == 'save':
            base, ext = os.path.splitext(path)
            new_path = base + '_font' + ext
            doc.saveas(new_path)
            print(f"저장 완료: {new_path}")

        elif cmd.isdigit():
            num = int(cmd)
            if num not in index_map:
                print("잘못된 번호입니다")
                continue

            style = index_map[num]
            old_font = style.dxf.font
            new_font = input("대체할 Windows font 파일명 [malgun.ttf]: ").strip()
            if not new_font:
                new_font = 'malgun.ttf'

            replace_font(style, new_font)
            print(f"Style '{style.dxf.name}' : {old_font} → {new_font}")

        else:
            print("알 수 없는 명령입니다")


if __name__ == '__main__':
    main()
