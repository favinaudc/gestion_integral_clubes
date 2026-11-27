def dni_desde_cuit_cuil(cuit_cuil: str) -> str:
    if len(cuit_cuil) != 11 or not cuit_cuil.isascii() or not cuit_cuil.isdigit():
        raise ValueError("El CUIT/CUIL debe tener exactamente 11 dígitos.")

    return cuit_cuil[2:-1]
