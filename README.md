# ✊ ✋ ✌️ Jokenpo com Webcam

Jogo de pedra, papel e tesoura contra o computador, em que você joga fazendo o gesto com a mão na frente da webcam. Feito em Python com OpenCV e MediaPipe.

- [Instalação](#instalação-windows)
- [Como jogar](#como-jogar)
- [Problemas comuns](#problemas-comuns)

---

## Instalação (Windows)

Você vai precisar de uma **webcam**, de **internet** para baixar o Python e as bibliotecas (só na primeira vez) e destes arquivos do jogo, todos juntos numa mesma pasta:

| Arquivo | Para que serve |
|---|---|
| `jokenpo.py` | O jogo. |
| `requirements.txt` | Lista de bibliotecas que o jogo usa. |
| `hand_landmarker.task` | Modelo que reconhece a mão. É opcional: se faltar, o jogo baixa sozinho na primeira vez que abrir. |

### 1. Instale o Python

Acesse [python.org/downloads](https://www.python.org/downloads/), baixe o **Python 3.14** e execute o instalador.

> [!IMPORTANT]
> Na primeira tela do instalador, **marque a caixa “Add python.exe to PATH”** antes de clicar em *Install Now*. Se esquecer, o comando `python` não vai funcionar.

Para instalar pelo terminal em vez do site, use:

```
winget install Python.Python.3.14
```

### 2. Confira se o Python foi instalado

Feche e abra de novo qualquer terminal. Abra o menu Iniciar, digite `cmd`, abra o *Prompt de Comando* e rode:

```
python --version
```

Deve aparecer algo como `Python 3.14.x`. Se a Microsoft Store abrir, ou se aparecer *“não é reconhecido”*, veja [Problemas comuns](#problemas-comuns).

### 3. Abra um terminal na pasta do jogo

No Explorador de Arquivos, entre na pasta com os arquivos do jogo, clique na **barra de endereço**, apague o que estiver escrito, digite `cmd` e aperte <kbd>Enter</kbd>. Um terminal abre direto nessa pasta.

### 4. Crie o ambiente virtual (venv)

O venv é uma pasta com uma cópia do Python só para este jogo, para as bibliotecas dele não se misturarem com as do resto do computador.

```
python -m venv venv
```

### 5. Instale as bibliotecas

Baixa o MediaPipe (reconhecimento da mão) e o OpenCV (webcam e janela). Pode levar alguns minutos.

```
venv\Scripts\python -m pip install -r requirements.txt
```

### 6. Abra o jogo

```
venv\Scripts\python jokenpo.py
```

A janela da webcam deve abrir. Mensagens de aviso do MediaPipe no terminal (linhas começando com `W0000` ou `INFO`) são normais e podem ser ignoradas.

### Das próximas vezes

Os passos 1 a 5 só são feitos uma vez. Depois, basta abrir o terminal na pasta do jogo (passo 3) e rodar:

```
venv\Scripts\python jokenpo.py
```

---

## Como jogar

Você joga contra o computador, que escolhe a jogada dele ao acaso. Mostre a mão para a webcam fazendo um dos três gestos:

| Gesto | Como fazer |
|:---:|---|
| ✊ **Pedra** | Mão fechada, todos os dedos dobrados. |
| ✋ **Papel** | Mão aberta, os quatro dedos esticados. |
| ✌️ **Tesoura** | Só o indicador e o médio esticados. |

### Quem ganha

- ✊ Pedra quebra ✌️ Tesoura
- ✌️ Tesoura corta ✋ Papel
- ✋ Papel embrulha ✊ Pedra

Jogadas iguais dão **empate**.

### Uma rodada, passo a passo

1. Deixe a mão visível para a câmera. No canto inferior da tela, **“Gesto:”** mostra o que o jogo está reconhecendo naquele instante. Use isso para ajustar a posição da mão.
2. Aperte <kbd>Espaço</kbd>. Começa a contagem **JO… KEN… PO!**
3. Quando aparecer **PO!**, faça o gesto e segure por um instante. O jogo lê a mão por menos de meio segundo.
4. Aparecem a sua jogada, a do computador e quem venceu. O placar no topo é atualizado.
5. Aperte <kbd>Espaço</kbd> de novo para a próxima rodada.

### Teclas

| Tecla | O que faz |
|---|---|
| <kbd>Espaço</kbd> | Começa uma rodada |
| <kbd>R</kbd> | Zera o placar |
| <kbd>Q</kbd> ou <kbd>Esc</kbd> | Fecha o jogo |

As teclas só funcionam com a janela do jogo selecionada. Se não responderem, clique uma vez na janela.

### Dicas para o jogo reconhecer melhor

- Deixe **a mão inteira, com o pulso**, dentro da imagem, a uns 40–80 cm da câmera.
- Jogue num lugar **bem iluminado**, sem luz forte atrás de você.
- Mostre só **uma mão** por vez.
- O polegar não conta: na tesoura, tanto faz ele estar aberto ou dobrado.
- Se aparecer *“Nao reconheci sua mao”*, a mão não apareceu direito no “PO!”. É só jogar de novo.

---

## Problemas comuns

<details>
<summary><code>python</code> “não é reconhecido como um comando” ou a Microsoft Store abre</summary>

O Python não foi adicionado ao PATH. Rode o instalador do Python de novo, escolha *Modify* (ou desinstale e instale outra vez) e **marque “Add python.exe to PATH”**. Depois feche e abra o terminal.

Se a Microsoft Store continuar abrindo, vá em *Configurações → Aplicativos → Configurações avançadas de aplicativos → Aliases de execução de aplicativo* e desligue *python.exe* e *python3.exe*.

</details>

<details>
<summary>Erro ao instalar: “No matching distribution found for mediapipe”</summary>

A versão do Python instalada não é compatível com essa versão do MediaPipe. O jogo foi testado no **Python 3.14**: confira com `python --version` e, se for outra versão, instale a 3.14.

Outra saída é abrir o `requirements.txt`, apagar os números de versão (deixar só `mediapipe` e `opencv-contrib-python`) e rodar a instalação de novo, para o pip escolher versões compatíveis.

</details>

<details>
<summary>“Nao foi possivel abrir a webcam”</summary>

- Feche outros programas que possam estar usando a câmera (Teams, Zoom, Meet no navegador etc.).
- Em *Configurações → Privacidade e segurança → Câmera*, deixe ligados **“Acesso à câmera”** e **“Permitir que aplicativos da área de trabalho acessem a câmera”**.
- Se o computador tiver mais de uma câmera e abrir a errada, edite o `jokenpo.py` e troque `cv2.VideoCapture(0` por `cv2.VideoCapture(1`.

</details>

<details>
<summary>Erro ao baixar o <code>hand_landmarker.task</code></summary>

Na primeira vez, sem esse arquivo na pasta, o jogo precisa de internet para baixá-lo. Conecte-se à internet ou copie o arquivo `hand_landmarker.task` do computador original para a pasta do jogo.

</details>

<details>
<summary>O jogo está lento ou travando</summary>

Feche outros programas pesados. O reconhecimento da mão roda no processador, e computadores mais antigos podem ficar com a imagem um pouco atrasada, mas o jogo continua funcionando.

</details>
