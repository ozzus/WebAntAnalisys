from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from pathlib import Path
import tempfile
from converter.side_parser import parse_side_file
from converter.gherkin_builder import build_gherkin

app = FastAPI(
    title="SIDE to Gherkin Converter API",
    description="API для конвертации Selenium .side файлов в Gherkin сценарии",
    version="1.0.0"
)


@app.post("/convert", response_class=PlainTextResponse)
async def convert_side_to_gherkin(file: UploadFile = File(...)):

    try:
        # Сохраняем временный файл
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Конвертация
        data = parse_side_file(tmp_path)
        gherkin = build_gherkin(data)

        return gherkin

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Conversion error: {str(e)}"
        )
    finally:
        # Удаляем временный файл
        if tmp_path:
            Path(tmp_path).unlink(missing_ok=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
