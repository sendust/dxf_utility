import ezdxf
import os

def change_text_font(dxf_filepath, new_font='malgum.ttf', output_suffix='_malgum'):
    """
    DXF 파일을 읽고, 모든 TEXT 및 MTEXT 엔티티의 폰트를 지정된 폰트로 변경합니다.

    :param dxf_filepath: 읽을 DXF 파일의 경로 (str)
    :param new_font: 적용할 새 폰트 파일 이름 (str, 예: 'malgum.ttf')
    :param output_suffix: 수정된 파일을 저장할 때 파일 이름에 추가할 접미사 (str)
    """
    print(f"DXF 파일 로드 중: {dxf_filepath}")
    
    try:
        # 1. DXF 파일 로드
        doc = ezdxf.readfile(dxf_filepath)
        
    except ezdxf.DXFError as e:
        print(f"DXF 파일 로드 중 오류 발생: {e}")
        return
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다. 경로를 확인해주세요: {dxf_filepath}")
        return

    # 모델스페이스(가장 일반적인 도면 공간) 가져오기
    msp = doc.modelspace()
    
    text_count = 0
    
    # 2. 모든 엔티티 반복 및 폰트 변경
    for entity in msp:
        # TEXT 또는 MTEXT 엔티티인지 확인
        if entity.dxftype() in ('TEXT', 'MTEXT'):
            try:
                # 폰트 변경을 위해 기존 스타일 가져오기 또는 새 스타일 생성
                # ezdxf는 폰트 설정을 DXF STYLE 테이블 엔티티를 통해 관리합니다.
                
                # 엔티티가 사용하는 스타일 이름 가져오기
                style_name = entity.dxf.style
                
                # 해당 스타일 정의 객체 가져오기
                style = doc.styles.get(style_name)

                # STYLE 엔티티의 폰트 설정 변경
                # primary_font_file 또는 font 속성을 사용합니다.
                # 새 폰트로 설정: "malgum.ttf"
                style.dxf.font = new_font
                
                text_count += 1
                
            except ezdxf.NoSuchEntityError:
                print(f"경고: 엔티티 {entity.dxf.handle} 가 참조하는 스타일 '{style_name}'을 찾을 수 없습니다.")
            except AttributeError as e:
                # 일부 TEXT/MTEXT 엔티티가 스타일을 올바르게 참조하지 않을 경우
                print(f"경고: 엔티티 {entity.dxftype()} 처리 중 오류 발생: {e}")


    print(f"총 {text_count}개의 TEXT/MTEXT 엔티티의 폰트 스타일을 '{new_font}'로 변경했습니다.")

    # 4. 수정된 파일 저장
    base, ext = os.path.splitext(dxf_filepath)
    output_filepath = f"{base}{output_suffix}{ext}"
    
    try:
        doc.saveas(output_filepath)
        print(f"수정된 파일이 성공적으로 저장되었습니다: {output_filepath}")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")

# --- 사용 예시 ---
# ⚠️ 중요: 아래 'your_file.dxf'를 실제 DXF 파일 경로로 변경해주세요.

dxf_file_path = input("DXF 파일 경로를 입력하세요: ").strip('"')
if not os.path.exists(dxf_file_path):
    print("파일이 존재하지 않습니다")
    exit()


print("\n--- 스크립트 실행 시작 ---")

change_text_font(dxf_file_path)

