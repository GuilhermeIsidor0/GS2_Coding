import re
 
#categorias que o usuário pode escolher
CATEGORIAS = {"buraco", "iluminacao", "lixo", "calcada", "outro"}
 
#situações possíveis de uma ocorrência 
STATUS = {"aberta", "em_andamento", "resolvida"}
 
 
def validar_cadastro(dados):
    #confere se os dados chegaram no formato correto
    if not isinstance(dados, dict):
        return None, "Envie um objeto JSON válido."
    #esse dic define os campos obrigatórios e o tamanho máximo de cada um
    campos = {
        "titulo": 100,
        "descricao": 500,
        "rua": 120,
        "bairro": 80,
        "cidade": 80
    }
    limpos = {}
    # verifica se os campos foram preenchidos corretamente
    for campo, tamanho in campos.items():
        valor = dados.get(campo)
        if not isinstance(valor, str) or not 1 <= len(valor.strip()) <= tamanho:
            return None, f"Preencha {campo} com até {tamanho} caracteres."
        # remove espaços desnecessários antes de salvar
        limpos[campo] = valor.strip()
    # verifica se a categoria escolhida existe
    categoria = dados.get("categoria")
    if categoria not in CATEGORIAS:
        return None, "Categoria inválida."
    # remove o traço do cep (pra nao dar conflito) e confere se tem 8 números
    cep = str(dados.get("cep", "")).replace("-", "")
    if not re.fullmatch(r"\d{8}", cep):
        return None, "O CEP deve ter 8 números."
    # verifica se o estado foi informado com duas letras
    uf = dados.get("uf")
    if not isinstance(uf, str) or not re.fullmatch(r"[A-Za-z]{2}", uf):
        return None, "UF inválida."
    # junta os dados que já foram validados
    limpos.update(categoria=categoria, cep=cep, uf=uf.upper())
    #retorna os dados prontos para serem cadastrados
    return limpos, None
 
 
def validar_status(dados):
    # verifica se o novo status é permitido
    if not isinstance(dados, dict) or dados.get("status") not in STATUS:
        return None, "Status inválido."
    # retorna o status para atualizar a ocorrência
    return {"status": dados["status"]}, None