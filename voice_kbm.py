import speech_recognition as sr
import keyboard
import pyautogui
import time

# Inicializa o reconhecimento de voz
recognizer = sr.Recognizer()

# Dicionário de comandos de voz para teclas do teclado e ações do mouse
commands = {
    "andar": "hold w",
    "parar": "release w; release a; release s; release d",
    "atacar": "click left",
    "atacar atacar": "click left; wait 0.25; click left",
    "canhoto": "click right",
    "canhotinho": "click right; wait 0.25; click right;",
    "canhotão": "click right; wait 0.25; click right; wait 0.25; click right",
    "esquivar": "press space; wait 0.05; release space",
    "defender": "hold shift; wait 0.025; release shift",
    "parar de defender": "release shift",
    "olhar para cima": "press u; wait 0.5; release u",
    "olhar para baixo": "press j; wait 0.5; release j",
    "olhar para esquerda": "press h; wait 0.5; release h",
    "olhar para direita": "press k; wait 0.5; release k",
    "andar para esquerda": "hold a",
    "andar para direita": "hold d",
    "andar para trás": "hold s",
    "parar de andar para esquerda": "release a",
    "parar de andar para direita": "release d",
    "parar de andar para trás": "release s"
}

def execute_command(command):
    for action in command.split(';'):
        action = action.strip()
        if action.startswith("hold"):
            key = action.split(" ")[1]
            keyboard.press(key)
            time.sleep(0.025)  # Garante que o botão seja pressionado por pelo menos 25 ms
        elif action.startswith("release"):
            key = action.split(" ")[1]
            keyboard.release(key)
        elif action.startswith("press"):
            key = action.split(" ")[1]
            keyboard.press_and_release(key)
            time.sleep(0.025)  # Garante que o botão seja pressionado por pelo menos 25 ms
        elif action.startswith("click"):
            button = action.split(" ")[1]
            if button == "left":
                for _ in range(3):
                    pyautogui.click(button='left')
                    time.sleep(0.25)
            elif button == "right":
                pyautogui.click(button='right')
        elif action.startswith("move mouse"):
            direction = action.split(" ")[2]
            if direction in ["up", "down", "left", "right"]:
                move_x = 0
                move_y = 0
                if direction == "up":
                    move_y = -10
                elif direction == "down":
                    move_y = 10
                elif direction == "left":
                    move_x = -10
                elif direction == "right":
                    move_x = 10
                pyautogui.moveRel(move_x, move_y)
        elif action.startswith("wait"):
            time.sleep(float(action.split(" ")[1]))

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Diga algo!")
        audio = recognizer.listen(source, phrase_time_limit=2)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language="pt-BR")
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["success"] = False
        response["error"] = "Unable to recognize speech"

    return response

# Loop principal
if __name__ == "__main__":
    mic = sr.Microphone()

    while True:
        print("Aguardando comando...")
        result = recognize_speech_from_mic(recognizer, mic)

        if result["transcription"]:
            commands_list = result["transcription"].lower().split(" e ")
            print(f"Você disse: {commands_list}")

            for command in commands_list:
                if command in commands:
                    execute_command(commands[command])
                else:
                    print("Comando não reconhecido")
        
        if result["error"]:
            print(f"ERROR: {result['error']}")