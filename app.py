# app.py — mock da Action /ocr_parse
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

app = FastAPI()

class Layer(BaseModel):
    odds: Optional[float] = None
    size: Optional[float] = None
    rank: int

class Row(BaseModel):
    selection: str
    back: List[Layer]
    lay: List[Layer]

class OCRRequest(BaseModel):
    jogo_id: Optional[str] = None
    filename: Optional[str] = None
    image_base64: Optional[str] = None
    market_hint: Optional[str] = None

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/ocr_parse")
def ocr_parse(req: OCRRequest) -> Dict[str, Any]:
    """
    MOCK para validar o fluxo. 
    Ele ignora a imagem e devolve um exemplo no formato combinado.
    Depois trocaremos pelo OCR real.
    """
    # Exemplo: se a dica tiver 'Resultado Final', devolve 1X2
    if (req.market_hint or "").lower().startswith("resultado final"):
        return {
            "market": "Resultado Final",
            "line": None,
            "header": {
                "home": "Santos FC",
                "away": "Grêmio FBPA",
                "kickoff": "01/10/2025 21:30"
            },
            "rows": [
                {
                    "selection": "Santos FC",
                    "back": [{"odds": 1.79, "size": 8104, "rank": 0},
                             {"odds": 1.78, "size": 7907, "rank": -1},
                             {"odds": 1.77, "size": 4035, "rank": -2}],
                    "lay":  [{"odds": 1.80, "size": 100, "rank": 0},
                             {"odds": 1.81, "size": 5147, "rank": +1},
                             {"odds": 1.82, "size": 9980, "rank": +2}]
                },
                {
                    "selection": "Grêmio FBPA",
                    "back": [{"odds": 5.7, "size": 4, "rank": 0},
                             {"odds": 5.6, "size": 3015, "rank": -1},
                             {"odds": 5.5, "size": 5398, "rank": -2}],
                    "lay":  [{"odds": 5.8, "size": 1225, "rank": 0},
                             {"odds": 5.9, "size": 2614, "rank": +1},
                             {"odds": 6.0, "size": 9439, "rank": +2}]
                },
                {
                    "selection": "Empate",
                    "back": [{"odds": 3.70, "size": 2532, "rank": 0},
                             {"odds": 3.65, "size": 14056, "rank": -1},
                             {"odds": 3.60, "size": 13207, "rank": -2}],
                    "lay":  [{"odds": 3.75, "size": 4, "rank": 0},
                             {"odds": 3.80, "size": 4109, "rank": +1},
                             {"odds": 3.85, "size": 3599, "rank": +2}]
                }
            ],
            "src": req.filename or "resultado_final.png",
            "confidence": 1.0
        }

    # Exemplo: se a dica tiver 'Ambas marcam', devolve BTTS
    if (req.market_hint or "").lower().startswith("ambas marcam"):
        return {
            "market": "Ambas marcam",
            "line": None,
            "rows": [
                {
                    "selection": "Sim",
                    "back": [{"odds":2.10,"size":1311,"rank":0},
                             {"odds":2.08,"size":5083,"rank":-1},
                             {"odds":2.06,"size":10717,"rank":-2}],
                    "lay":  [{"odds":2.14,"size":4004,"rank":0},
                             {"odds":2.16,"size":3589,"rank":+1},
                             {"odds":2.18,"size":7282,"rank":+2}]
                },
                {
                    "selection": "Não",
                    "back": [{"odds":1.88,"size":61085,"rank":0},
                             {"odds":1.87,"size":34526,"rank":-1},
                             {"odds":1.86,"size":4612,"rank":-2}],
                    "lay":  [{"odds":1.91,"size":1892,"rank":0},
                             {"odds":1.92,"size":368,"rank":+1},
                             {"odds":1.93,"size":54297,"rank":+2}]
                }
            ],
            "src": req.filename or "btts.png",
            "confidence": 1.0
        }

    # Default genérico:
    return {
        "market": "Desconhecido",
        "line": None,
        "rows": [],
        "src": req.filename or "image.png",
        "confidence": 1.0
    }
