# -*- coding: utf-8 -*-
"""
Servicio de IA para retroalimentación personalizada basada en el perfil CT.
Autor: Luis Carlos Valencia
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

# Perfil CT fijo (contexto permanente)
PERFIL_CT = """
**Perfil Temperamental: Autístico - Normaloide con matiz Epileptoide**

**Fortalezas clave:**
- Decisiones pensadas y ponderadas con análisis profundo del impacto en otros.
- Visión de detalle, organización y capacidad para estructurar proyectos complejos.
- Capacidad de escucha orientada a soluciones (enfoque técnico/racional).
- Sentido de responsabilidad y orgullo de pertenencia.

**Áreas de atención (puntos ciegos):**
- Análisis → Sobreanálisis (parálisis por análisis).
- Calidad → Perfeccionismo (pérdida de eficiencia por buscar la mejora innecesaria).
- Orden → Rigidez (dificultad para adaptarse a imprevistos o cambios de proceso).
- Responsabilidad → Dificultad para delegar (cargar con tareas que corresponden a otros).
- Dificultad para gestionar la complejidad humana/emocional (prefiere soluciones técnicas).
"""

def get_ai_feedback(record_data):
    """
    Envía el registro semanal a Deepseek y recibe retroalimentación personalizada.
    
    Args:
        record_data (dict): Datos del registro semanal
        
    Returns:
        str: Retroalimentación generada por la IA
    """
    if not DEEPSEEK_API_KEY:
        return "⚠️ API Key de Deepseek no configurada. Por favor, añádela a tu archivo .env"

    # Temperatura fija en 0.2 para reflexión profunda y coherente
    temperatura = 0.2
    
    # Construir el prompt
    prompt = construir_prompt(record_data)
    
    # System prompt con tono paisa (Catalina, de Medellín)
    system_prompt = """
Eres una coach ejecutiva con más de 15 años de experiencia en liderazgo y desarrollo personal, especializada en perfiles temperamentales (CT). Te llamas Catalina y eres de Medellín, Colombia.

**Tu filosofía de trabajo:**
El objetivo NO es cambiar quién es la persona, sino ayudarla a UTILIZAR CONSCIENTEMENTE sus fortalezas y DESARROLLAR las capacidades que las complementan. Trabajas siempre desde la esencia del perfil temperamental, nunca en contra de él.

**Tu estilo de comunicación (Muy importante):**
- Hablas con "usted" (respetuoso y cercano a la vez, como la gente de Medellín).
- Usas un tono cálido, maternal y empático. Haces sentir a la persona como si estuviera en una conversación de café.
- Usas diminutivos cariñosos: "ahorita", "rapidito", "poquito", "detallito", "cosita".
- Usas muletillas suaves como: "¿sí?", "pues", "entonces", "o sea", "mire".
- Dices frases como: "Vamos bien", "Qué bonito", "No se me agüeve", "Con calma", "Hagamos un ajustecito".
- Hablas con claridad, sin rodeos, pero siempre con un abrazo en la voz.
- Eres directa cuando toca, pero nunca dura.

**NO USES anécdotas de fútbol, deportes en general, ni videojuegos.**
En su lugar, usa ejemplos de: dinámicas de equipo, relaciones interpersonales, gestión del tiempo, toma de decisiones, comunicación efectiva, desarrollo profesional.

Tu enfoque es ayudar a la persona a ser más consciente de sus fortalezas (Autístico-Normaloide con matiz Epileptoide) y a equilibrar sus puntos ciegos, siempre desde el respeto, la empatía y la comprensión de su naturaleza.
"""
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperatura,
        "max_tokens": 800
    }
    
    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        feedback = result["choices"][0]["message"]["content"]
        return feedback
    except Exception as e:
        return f"❌ Error al obtener retroalimentación: {str(e)}"


def construir_prompt(record_data):
    """
    Construye un prompt detallado usando el perfil CT y los datos del registro.
    """
    prompt = f"""
Basado en el siguiente perfil CT y en el registro semanal del usuario, 
proporciona una retroalimentación constructiva y personalizada.

**PRINCIPIO RECTOR:**
El objetivo no es cambiar quién eres, sino utilizar conscientemente tus fortalezas 
y desarrollar las capacidades que las complementan. Trabaja siempre desde la esencia 
del perfil Autístico-Normaloide con matiz Epileptoide.

---

## PERFIL CT DEL USUARIO:
{PERFIL_CT}

---

## REGISTRO SEMANAL:

**1. Potencial Personal:**
{record_data.get('potential_personal', 'No especificado')}

**1. Potencial Profesional:**
{record_data.get('potential_professional', 'No especificado')}

**Evidencias observadas:**
{record_data.get('evidence', 'No especificado')}

**2. Puntos Ciegos (Personal):**
{record_data.get('blindspot_personal', 'No especificado')}

**2. Puntos Ciegos (Profesional):**
{record_data.get('blindspot_professional', 'No especificado')}

**Puntos Ciegos identificados (marcados por el usuario):**
- Sobreanálisis: {record_data.get('blindspots', {}).get('sobreanalisis', False)}
- Perfeccionismo: {record_data.get('blindspots', {}).get('perfeccionismo', False)}
- Rigidez: {record_data.get('blindspots', {}).get('rigidez', False)}
- Responsabilidad: {record_data.get('blindspots', {}).get('responsabilidad', False)}

**3. Adaptación Personal:**
{record_data.get('adaptation_personal', 'No especificado')}

**3. Adaptación Profesional:**
{record_data.get('adaptation_professional', 'No especificado')}

**Comunicación:**
{record_data.get('communication', 'No especificado')}

**4. Hábitos diseñados:**
- Fortaleza aprovechada: {record_data.get('habit_strength', 'No especificado')}
- Desafío detectado: {record_data.get('habit_challenge', 'No especificado')}
- Hábito a practicar: {record_data.get('habit_practice', 'No especificado')}

**5. Auto-evaluación (1-5):**
- Análisis equilibrado: {record_data.get('analysis_score', 0)}/5
- Flexibilidad: {record_data.get('flexibility_score', 0)}/5
- Delegación: {record_data.get('delegation_score', 0)}/5
- Comunicación: {record_data.get('communication_score', 0)}/5
- Desarrollo de personas: {record_data.get('development_score', 0)}/5
- Serenidad ante incertidumbre: {record_data.get('serenity_score', 0)}/5
- Balance Personal-Profesional: {record_data.get('balance_score', 0)}/5

---

**INSTRUCCIONES PARA LA RETROALIMENTACIÓN:**

Por favor, proporciona un análisis estructurado en 3 secciones, siempre desde el respeto a su perfil temperamental:

1. **🎯 Reconocimiento de Fortalezas (desde tu esencia):**
   - Destaca 2-3 acciones concretas donde el usuario utilizó bien su perfil CT.
   - Relaciona estas acciones con sus fortalezas naturales (análisis, detalle, estructura, responsabilidad).
   - Reconoce el valor de su forma de ser, sin sugerir que debe cambiar.

2. **🔍 Áreas de Crecimiento (equilibrio, no cambio):**
   - Identifica 1-2 patrones que podrían estar limitando su efectividad.
   - Conecta estos patrones con sus puntos ciegos CT (sobreanálisis, perfeccionismo, rigidez, delegación).
   - Ofrece sugerencias para **equilibrar** sus fortalezas, no para eliminarlas.
   - Sé específico y evita generalidades.

3. **💡 Recomendación para la próxima semana (desde quién eres):**
   - Da 1 desafío concreto y accionable para la próxima semana.
   - El desafío debe ayudar a **utilizar mejor** una fortaleza o a **complementar** un punto ciego.
   - Asegúrate de que el desafío sea coherente con su perfil (ej: si sobreanaliza, proponer un tiempo límite para decidir, no "deja de analizar").
   - Incluye una frase motivacional corta que refuerce su identidad.

**Recuerda:** Habla como una mujer de Medellín. Usa "usted", sé cálida, usa diminutivos y muletillas paisas. Que Luis Carlos sienta que está hablando con una coach que le habla con el alma. Sin fútbol, sin deportes, sin videojuegos.
"""

    return prompt