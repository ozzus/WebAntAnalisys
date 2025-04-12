import os
import argparse
from converter.side_parser import parse_side_file
from converter.gherkin_builder import build_gherkin

def convert_side_to_gherkin(input_path: str, output_dir: str):
    """Основной процесс конвертации"""
    try:
        # Валидация входных данных
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Парсинг и генерация
        data = parse_side_file(input_path)
        gherkin = build_gherkin(data)
        
        # Создание выходной директории
        os.makedirs(output_dir, exist_ok=True)
        
        # Формирование имени выходного файла
        base_name = os.path.basename(input_path)
        output_file = os.path.join(
            output_dir,
            base_name.replace(".side", ".feature")
        )
        
        # Сохранение результата
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(gherkin)
        
        print(f"Successfully converted: {input_path} -> {output_file}")
    
    except Exception as e:
        print(f"Conversion failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Selenium .side files to Gherkin"
    )
    parser.add_argument(
        "-i", 
        "--input", 
        default="examples/login_test.side",
        help="Input .side file path"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="features",
        help="Output directory for .feature files"
    )
    
    args = parser.parse_args()
    convert_side_to_gherkin(args.input, args.output)