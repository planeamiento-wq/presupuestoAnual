import streamlit as st

def crear_tabla_consolidado(datos_calculados):
    """
    Renderiza la tabla de cascada presupuestaria clonando el diseño del PPT.
    Recibe un diccionario con los valores numéricos calculados en tiempo real.
    """
    
    # Desempaquetamos los valores del diccionario
    c = datos_calculados

    # Formateadores internos de la tabla
    def f_pos(v):
        return f"$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def f_neg(v):
        num = f"$ {abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f'<span style="color: #dc3545;">-$ {num[2:]}</span>'

    # Estilos CSS específicos para clonar la tabla del PPT
    st.markdown("""
        <style>
        .tabla-unsta {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Source Sans Pro', sans-serif;
            color: #333333;
            background-color: #ffffff;
        }
        .tabla-unsta tr {
            border-bottom: 1px solid #f1f1f1;
        }
        .tabla-unsta td {
            padding: 8px 12px;
            font-size: 12px;
            vertical-align: middle;
        }
        /* Filas de Subtotales y Resultados (Fondo Gris Claro) */
        .fila-resultado {
            background-color: #f2f6f9 !important;
            font-weight: bold;
        }
        .text-verde {
            color: #198754;
            font-weight: bold;
        }
        .col-signo {
            width: 3%;
            text-align: left;
            font-weight: bold;
            color: #555555;
        }
        .col-concepto {
            width: 52%;
            text-align: left;
        }
        .col-monto {
            width: 30%;
            text-align: right;
            font-family: monospace;
            font-size: 14px;
        }
        .col-margen {
            width: 15%;
            text-align: right;
            font-size: 18px;
            font-weight: bold;
            color: #212529;
            border-left: 2px solid #e2e8f0;
            padding-right: 15px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Construcción de la matriz HTML siguiendo la imagen del PPT
    html = f"""
    <table class="tabla-unsta">
        <tr>
            <td class="col-signo"></td>
            <td class="col-concepto">INGR. CUOTAS DE GRADO</td>
            <td class="col-monto text-verde">{f_pos(c['ing_cuotas_grado'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr>
            <td class="col-signo">-</td>
            <td class="col-concepto">BONIFICACIONES</td>
            <td class="col-monto">{f_neg(c['bonificaciones'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr>
            <td class="col-signo">-</td>
            <td class="col-concepto">REDUCC. BECAS</td>
            <td class="col-monto">{f_neg(c['reduc_becas'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr>
            <td class="col-signo">-</td>
            <td class="col-concepto">REDUCC. SEDE</td>
            <td class="col-monto">{f_neg(c['reduc_sede'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr class="fila-resultado">
            <td class="col-signo">=</td>
            <td class="col-concepto">INGRESOS NETOS</td>
            <td class="col-monto text-verde">{f_pos(c['ingresos_netos'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr>
            <td class="col-signo">+</td>
            <td class="col-concepto">INGR. MATRICULAS DE GRADO</td>
            <td class="col-monto text-verde">{f_pos(c['ing_matriculas'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr>
            <td class="col-signo">+</td>
            <td class="col-concepto">CURSOS EXTENSION</td>
            <td class="col-monto text-verde">{f_pos(c['cursos_extension'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr>
            <td class="col-signo">+</td>
            <td class="col-concepto">INGRESOS VARIOS</td>
            <td class="col-monto text-verde">{f_pos(c['ingresos_varios'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr>
            <td class="col-signo">-</td>
            <td class="col-concepto">GASTOS EN PERSONAL</td>
            <td class="col-monto">{f_neg(c['gastos_personal'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr>
            <td class="col-signo">-</td>
            <td class="col-concepto">GASTOS DE FUNCIONAMIENTO</td>
            <td class="col-monto">{f_neg(c['gastos_funcionamiento'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr>
            <td class="col-signo">-</td>
            <td class="col-concepto">INVERSIONES OPERATIVAS</td>
            <td class="col-monto">{f_neg(c['inversiones_operativas'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr class="fila-resultado">
            <td class="col-signo">=</td>
            <td class="col-concepto">RESULTADO OPERATIVO (EXCL. ING. FCIEROS)</td>
            <td class="col-monto" style="color: {'#212529' if c['resultado_operativo_excl'] >= 0 else '#dc3545'};">
                {f_pos(c['resultado_operativo_excl']) if c['resultado_operativo_excl'] >= 0 else f_neg(c['resultado_operativo_excl'])}
            </td>
            <td class="col-margen">{c['margen_excl']:.1f}%</td>
        </tr>
        <tr>
            <td class="col-signo">+</td>
            <td class="col-concepto">INGR. FINANCIEROS</td>
            <td class="col-monto text-verde">{f_pos(c['ing_financieros'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr class="fila-resultado">
            <td class="col-signo">=</td>
            <td class="col-concepto">RESULTADO OPERATIVO (INCL. ING. FCIEROS.)</td>
            <td class="col-monto" style="color: {'#212529' if c['resultado_operativo_incl'] >= 0 else '#dc3545'};">
                {f_pos(c['resultado_operativo_incl']) if c['resultado_operativo_incl'] >= 0 else f_neg(c['resultado_operativo_incl'])}
            </td>
            <td class="col-margen">{c['margen_incl']:.1f}%</td>
        </tr>
        <tr>
            <td class="col-signo">-</td>
            <td class="col-concepto">INVERSIONES OBRAS</td>
            <td class="col-monto">{f_neg(c['inversiones_obra'])}</td>
            <td class="col-margen"></td>
        </tr>
        <tr class="fila-resultado" style="border-bottom: 2px solid #cbd5e1;">
            <td class="col-signo">=</td>
            <td class="col-concepto">RESULTADO OPERATIVO INCL. INVERS. OBRAS.</td>
            <td class="col-monto" style="color: {'#212529' if c['resultado_final'] >= 0 else '#dc3545'};">
                {f_pos(c['resultado_final']) if c['resultado_final'] >= 0 else f_neg(c['resultado_final'])}
            </td>
            <td class="col-margen">{c['margen_final']:.1f}%</td>
        </tr>
    </table>
    """
    
    st.markdown(html, unsafe_allow_html=True)