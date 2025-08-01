from __future__ import annotations
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from automatos import AFD, AP
from gramatica_livre_contexto import conversao_AFD_para_GLC, conversao_GLC_para_AP, GLC


def demonstracao_afd_para_glc():
    print("="*50)
    print("INÍCIO DA DEMONSTRAÇÃO 1: AFD -> GLC")
    print("="*50)

    # 1. Crie o AFD de exemplo (aceita cadeias que terminam com 'b')
    afd_exemplo = AFD(
        estados={'q0', 'q1'},
        alfabeto={'a', 'b'},
        transicoes={
            'q0': {'a': 'q0', 'b': 'q1'},
            'q1': {'a': 'q0', 'b': 'q1'}
        },
        estado_inicial='q0',
        estados_finais={'q1'}
    )
    print("Passo 1: Definimos o seguinte AFD:")
    print(afd_exemplo)

    # 2. função de conversão
    print("\nPasso 2: Executando a função conversao_AFD_para_GLC...")
    glc_resultante = conversao_AFD_para_GLC(afd_exemplo)
    print("✔ Conversão concluída!")

    # 3. resultado
    print("\nPasso 3: A Gramática Livre de Contexto resultante é:")
    print(glc_resultante)
    print("="*50)
    print("FIM DA DEMONSTRAÇÃO 1")
    print("="*50 + "\n")


def demonstracao_glc_para_ap():
    print("="*50)
    print("INÍCIO DA DEMONSTRAÇÃO 2: GLC -> AP")
    print("="*50)

    # 1. Crie a GLC de exemplo para L = {0^n 1^n | n >= 0}
    glc_exemplo = GLC(
        V={'S'},
        E={'0', '1'},
        S='S',
        R={
            'S': [
                ['0', 'S', '1'],
                ['ε']
            ]
        }
    )
    print("Passo 1: Definimos a seguinte GLC (para a linguagem não-regular 0^n 1^n):")
    print(glc_exemplo)

    print("\nPasso 2: Executando a função conversao_GLC_para_AP...")
    try:
        ap_resultante = conversao_GLC_para_AP(glc_exemplo)
        print("✔ Conversão concluída!")

        print("\nPasso 3: O Autômato com Pilha resultante é:")
        print(ap_resultante)
    except Exception as e:
        print(f"Ocorreu um erro durante a conversão: {e}")
        import traceback
        traceback.print_exc()

    print("="*50)
    print("FIM DA DEMONSTRAÇÃO 2")
    print("="*50)


if __name__ == "__main__":
    # demonstracao_afd_para_glc()
    demonstracao_glc_para_ap()