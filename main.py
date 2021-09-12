import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIDTH_LOCALS


def calc_imc(
    peso: float,
    altura: float
) -> float:
    return peso / (altura * altura)


def get_imcs(
    file_name: str
) -> dict:
    imcs = {
        "sexo": [],
        "peso (kg)": [],
        "altura (m)": [],
        "imc": [],
        "condição": []
    }

    try:
        with open(
            file=file_name,
            mode="r",
            encoding="utf-8"
        ) as file:
            for row in [r for r in file][1:]:
                s, p, a, i, c = row.split(",")

                imcs["sexo"].append(s)
                imcs["peso (kg)"].append(float(p))
                imcs["altura (m)"].append(float(a))
                imcs["imc"].append(float(i))
                imcs["condição"].append(c)
    
    except:
        with open(
            file=file_name,
            mode="w",
            encoding="utf-8"
        ) as file:
            file.write(",".join(imcs.keys()))
    
    return imcs


def is_float(
    string: str
) -> bool:
    try:
        float(string)
        return True
    
    except:
        return False


if __name__ == "__main__":
    file = "./imc.csv"

    imcs = get_imcs(file)
    qtd_imcs = len(imcs["imc"])

    se, pe, al, im, co = imcs.values()

    imc_list = [f"{se[i]}, {pe[i]:.2f}, {al[i]:.2f}, {im[i]:.2f}, {co[i]}".strip() for i in range(len(im))]

    sg.theme("DarkAmber")

    layout_window_1 = [
        [sg.Text("Sexo:", key="txt_sexo"), sg.Radio("Masculino", 1, key="m"), sg.Radio("Feminino", 1, key="f")],
        [sg.Text("Peso:", key="txt_peso"), sg.InputText(key="input_peso")],
        [sg.Text("Altura:", key="txt_altura"), sg.InputText(key="input_altura")],
        [sg.Button("Calcular"), sg.Button("Mostrar todos os IMCs")]
    ]

    layout_window_2 = [
        [sg.Column([
            [sg.Listbox(imc_list, size=(50, 10), key="list_box")],
            [sg.Button("Fechar")],
        ], element_justification="center")]
    ]

    window_1 = sg.Window("Calculadora de IMC", layout_window_1, finalize=True)
    window_2 = sg.Window("Lista dos IMCs", layout_window_2, finalize=True)
    window_2.hide()

    while True:
        ew1, vw1 = window_1.read()

        if ew1 == sg.WIN_CLOSED:
            break

        sexo = "f" if vw1["f"] else "m" if vw1["m"] else "ERRO"
        peso = vw1["input_peso"]
        altura = vw1["input_altura"]

        if ew1 == "Calcular":
            if (
                sexo != "ERRO"
                and is_float(peso)
                and is_float(altura)
            ):
                peso = float(peso)
                altura = float(altura)

                imc = calc_imc(peso, altura)

                imcs["sexo"].append(sexo)
                imcs["peso (kg)"].append(peso)
                imcs["altura (m)"].append(altura)
                imcs["imc"].append(imc)

                if sexo == "M":
                    condicao = (
                        "abaixo do peso"
                        if imc < 20.7 else
                        "peso normal"
                        if imc < 26.4 else
                        "marginalmente acima do peso"
                        if imc < 27.8 else
                        "acima do peso ideal"
                        if imc < 31.1 else
                        "obeso"
                    )
                
                else:
                    condicao = (
                        "abaixo do peso"
                        if imc < 19.1 else
                        "peso normal"
                        if imc < 25.8 else
                        "marginalmente acima do peso"
                        if imc < 27.3 else
                        "acima do peso ideal"
                        if imc < 32.3 else
                        "obeso"
                    )
                
                imcs["condição"].append(condicao)
                
                sg.popup(
                    f"Sexo: {'Feminino' if sexo == 'f' else 'Masculino'}\n"
                    f"Peso: {peso:.2f}kg\n"
                    f"Altura: {altura:.2f}m\n"
                    f"IMC: {imc:.2f}\n"
                    f"Condição: {condicao}\n"
                )

                window_1["input_peso"].update(value="")
                window_1["input_altura"].update(value="")
                window_1["f"].update(value=False)
                window_1["m"].update(value=False)
            
            else:
                sg.popup("Dados Inválidos!")
        
        elif ew1 == "Mostrar todos os IMCs":
            window_1.disable()
            window_2.un_hide()

            se, pe, al, im, co = imcs.values()

            imc_list = [f"{se[i]}, {pe[i]:.2f}, {al[i]:.2f}, {im[i]:.2f}, {co[i]}".strip() for i in range(len(im))]
            
            window_2.Element("list_box").Update(imc_list)

            while True:
                ew2, vw2 = window_2.read()

                if ew2 in [sg.WIN_CLOSED, "Fechar"]:
                    break

            window_2.hide()
            window_1.enable()

    with open(
        file=file,
        mode="a",
        encoding="utf-8"
    ) as file:
        se, pe, al, im, co = imcs.values()

        try:
            for i in range(qtd_imcs, len(im)):
                file.write(f"\n{se[i]},{pe[i]:.2f},{al[i]:.2f},{im[i]:.2f},{co[i]}")
        
        except:
            pass

    window_1.close()
