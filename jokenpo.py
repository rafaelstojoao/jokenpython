"""Jokenpo (pedra, papel e tesoura) com reconhecimento de mao via webcam.

Controles:
    ESPACO  -> inicia uma rodada (contagem JO-KEN-PO)
    R       -> zera o placar
    Q / ESC -> sai
"""

import random
import time
import urllib.request
from collections import Counter
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

MODEL_PATH = Path(__file__).with_name("hand_landmarker.task")
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)

PEDRA, PAPEL, TESOURA = "PEDRA", "PAPEL", "TESOURA"
JOGADAS = [PEDRA, PAPEL, TESOURA]
VENCE = {PEDRA: TESOURA, PAPEL: PEDRA, TESOURA: PAPEL}  # chave vence valor

CONTAGEM = ["JO", "KEN", "PO!"]
SEGUNDOS_POR_PALAVRA = 0.7
JANELA_CAPTURA = 0.4      # segundos lendo o gesto apos o "PO!"
TEMPO_RESULTADO = 3.0

# Conexoes entre os 21 pontos da mao, para desenhar o esqueleto
CONEXOES = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20), (0, 17),
]

# (ponta, articulacao PIP) de indicador, medio, anelar e minimo
DEDOS = [(8, 6), (12, 10), (16, 14), (20, 18)]


def garantir_modelo():
    if not MODEL_PATH.exists():
        print("Baixando modelo de deteccao de maos...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


def dist2(a, b):
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


def classificar(landmarks):
    """Retorna PEDRA, PAPEL, TESOURA ou None a partir dos 21 pontos da mao.

    Um dedo esta esticado quando a ponta fica mais longe do pulso do que a
    articulacao do meio - funciona com a mao em qualquer rotacao.
    """
    pulso = landmarks[0]
    esticados = [dist2(landmarks[p], pulso) > dist2(landmarks[j], pulso) * 1.1
                 for p, j in DEDOS]
    indicador, medio, anelar, minimo = esticados

    if not any(esticados):
        return PEDRA
    if all(esticados):
        return PAPEL
    if indicador and medio and not anelar and not minimo:
        return TESOURA
    return None


def resultado(jogador, cpu):
    if jogador == cpu:
        return "EMPATE", (0, 215, 255)
    if VENCE[jogador] == cpu:
        return "VOCE VENCEU!", (0, 200, 0)
    return "CPU VENCEU!", (0, 0, 230)


def desenhar_mao(frame, landmarks):
    h, w = frame.shape[:2]
    pts = [(int(p.x * w), int(p.y * h)) for p in landmarks]
    for a, b in CONEXOES:
        cv2.line(frame, pts[a], pts[b], (255, 255, 255), 2)
    for pt in pts:
        cv2.circle(frame, pt, 4, (255, 0, 180), -1)


def texto(frame, msg, pos, escala=1.0, cor=(255, 255, 255), espessura=2, centro=False):
    fonte = cv2.FONT_HERSHEY_DUPLEX
    if centro:
        (tw, _), _ = cv2.getTextSize(msg, fonte, escala, espessura)
        pos = ((frame.shape[1] - tw) // 2, pos[1])
    cv2.putText(frame, msg, pos, fonte, escala, (0, 0, 0), espessura + 4, cv2.LINE_AA)
    cv2.putText(frame, msg, pos, fonte, escala, cor, espessura, cv2.LINE_AA)


def main():
    garantir_modelo()
    opcoes = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
    )
    detector = vision.HandLandmarker.create_from_options(opcoes)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Nao foi possivel abrir a webcam.")

    placar = {"voce": 0, "cpu": 0, "empates": 0}
    estado = "espera"          # espera -> contagem -> captura -> resultado
    inicio_estado = 0.0
    leituras = []
    ultimo = None              # (jogador, cpu, mensagem, cor)
    inicio = time.monotonic()

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)  # espelha, como um espelho
        agora = time.monotonic()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagem = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        res = detector.detect_for_video(imagem, int((agora - inicio) * 1000))

        gesto = None
        if res.hand_landmarks:
            mao = res.hand_landmarks[0]
            desenhar_mao(frame, mao)
            gesto = classificar(mao)

        h = frame.shape[0]
        decorrido = agora - inicio_estado

        if estado == "espera":
            texto(frame, "ESPACO para jogar", (0, h // 2), 1.2, centro=True)
        elif estado == "contagem":
            i = int(decorrido / SEGUNDOS_POR_PALAVRA)
            if i < len(CONTAGEM):
                texto(frame, CONTAGEM[i], (0, h // 2), 3.0, (0, 255, 255), 5, centro=True)
            else:
                estado, inicio_estado, leituras = "captura", agora, []
        elif estado == "captura":
            texto(frame, "PO!", (0, h // 2), 3.0, (0, 255, 255), 5, centro=True)
            if gesto:
                leituras.append(gesto)
            if decorrido >= JANELA_CAPTURA:
                if leituras:
                    jogador = Counter(leituras).most_common(1)[0][0]
                    cpu = random.choice(JOGADAS)
                    msg, cor = resultado(jogador, cpu)
                    chave = {"EMPATE": "empates", "VOCE VENCEU!": "voce"}.get(msg, "cpu")
                    placar[chave] += 1
                    ultimo = (jogador, cpu, msg, cor)
                else:
                    ultimo = None
                estado, inicio_estado = "resultado", agora
        elif estado == "resultado":
            if ultimo:
                jogador, cpu, msg, cor = ultimo
                texto(frame, f"Voce: {jogador}", (0, h // 2 - 60), 1.2, centro=True)
                texto(frame, f"CPU: {cpu}", (0, h // 2), 1.2, centro=True)
                texto(frame, msg, (0, h // 2 + 70), 1.8, cor, 3, centro=True)
            else:
                texto(frame, "Nao reconheci sua mao :(", (0, h // 2), 1.1, (0, 0, 230), centro=True)
            if decorrido >= TEMPO_RESULTADO:
                estado = "espera"

        texto(frame, f"Voce {placar['voce']}  x  {placar['cpu']} CPU   (empates: {placar['empates']})",
              (15, 35), 0.8)
        texto(frame, f"Gesto: {gesto or '-'}", (15, h - 20), 0.8, (200, 255, 200))

        cv2.imshow("Jokenpo", frame)
        tecla = cv2.waitKey(1) & 0xFF
        if tecla in (ord("q"), 27) or cv2.getWindowProperty("Jokenpo", cv2.WND_PROP_VISIBLE) < 1:
            break
        if tecla == ord(" ") and estado == "espera":
            estado, inicio_estado = "contagem", agora
        if tecla == ord("r"):
            placar = dict.fromkeys(placar, 0)

    cap.release()
    detector.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
