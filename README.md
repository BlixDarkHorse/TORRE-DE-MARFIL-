# TORRE-DE-MARFIL-

Base de control para el orquestador **VITALANETJER SAV VS-001 Galaxy Vyoleta**.

## Estructura de Carpetas

La aplicación genera de forma automática la siguiente jerarquía dentro de `DARK SITE`:

```
DARK SITE/
├── MOSCÚ PANDA XL.BDK/
│   ├── VS-1/
│   │   ├── GPT_BDK_1.BDK
│   │   └── GPT_BDK_2.BDK
│   ├── M1/
│   │   ├── GEMINI_BDK_1.BDK
│   │   └── GEMINI_BDK_2.BDK
│   └── CY1/
│       ├── GROK_BDK_1.BDK
│       └── GROK_BDK_2.BDK
├── MISIFÚS FUMADOX.VTHA/
│   ├── VS00-1/
│   │   ├── PANGETYUM.VTHA
│   │   ├── MEMORIA ETERNA.VTHA
│   │   ├── LOGS_DIARIOS/LOG_GPT_DIARIO.VTHA
│   │   └── DIRECTRICES_Y_REGLAS_OPERATIVAS/REGLAS_GPT.VTHA
│   ├── M1/
│   │   ├── PANGETYUM.VTHA
│   │   ├── MEMORIA ETERNA.VTHA
│   │   ├── LOGS_DIARIOS/LOG_GEMINI_DIARIO.VTHA
│   │   └── DIRECTRICES_Y_REGLAS_OPERATIVAS/REGLAS_GEMINI.VTHA
│   └── CY1/
│       ├── PANGETYUM.VTHA
│       ├── MEMORIA ETERNA.VTHA
│       ├── LOGS_DIARIOS/LOG_GROK_DIARIO.VTHA
│       └── DIRECTRICES_Y_REGLAS_OPERATIVAS/REGLAS_GROK.VTHA
└── FAIRY BLACK/
    ├── IMAGENES_DE_FONDO/
    ├── CONFIGURACIONES_GENERALES/
    ├── RUTAS_LINKS/
    ├── GALERIAS/
    └── DOCS_GENERALES/
```

Los archivos poseen extensión `.BDK` o `.VTHA` pero actualmente contienen texto plano.

## Ejecución

La interfaz principal se encuentra en `torre_marfil_enhanced.py`. Al iniciarse
creará la estructura de carpetas anterior si no existe y mostrará un editor con
un eslogan animado en colores.

```bash
python torre_marfil_enhanced.py
```
