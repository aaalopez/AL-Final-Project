"""FINtellect - financial literacy app for older adults.

Dash entry point: layout, routing between sections, and callbacks that
call the Tutor, Scam-Checker, and Family-Bridge agents.
"""

from urllib.parse import quote

from dash import Dash, dcc, html, Input, Output, State, ALL, ctx
from dash.exceptions import PreventUpdate

from agents import tutor_agent, scam_checker_agent, family_bridge_agent, chat_agent
from agents.client import AgentError
from data.topics import TOPICS, get_category_labels, get_subtopics, get_subtopic_label
from data.misconceptions import MISCONCEPTIONS, get_misconception_label
from data.faqs import COMMON_QUESTIONS, get_question_label
from data.kids_investing import KIDS_INVESTING_TOPICS, get_kids_investing_label
from data.scam_types import COMMON_SCAM_TYPES, ORGANIZATIONS_SCAMMERS_IMPERSONATE

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "FINtellect"

LANGUAGE_OPTIONS = [
    {"label": "English", "value": "en"},
    {"label": "Español", "value": "es"},
    {"label": "Français", "value": "fr"},
]

UI_TEXT = {
    "en": {
        "nav_home": "Home",
        "nav_101s": "101s",
        "nav_misconceptions": "Misconceptions",
        "nav_scams": "Common Scams",
        "nav_for_kids": "Ask a Loved One",
        "nav_kids_investing": "Investing in My Kids",
        "nav_chat": "Ask a Question",
        "nav_faq": "Common Questions",
        "nav_profile": "Profile",
        "welcome": "Welcome",
        "welcome_text": "FINtellect helps you build financial confidence, at your own pace. Free to use, no account needed, no analytics or human reviewers — what you type is sent only to the AI model to generate your answer.",
        "home_101s": "101s",
        "home_101s_desc": "Plain-language guides on retirement, loans, savings, Social Security, Medicare, estate planning, insurance, and investing.",
        "home_101s_cta": "Browse the 101s",
        "home_myths": "Misconceptions",
        "home_myths_desc": "See common money myths explained — what's true, what's not, and why.",
        "home_myths_cta": "Check a myth",
        "home_scams": "Common Scams",
        "home_scams_desc": "Learn frequent scam patterns, and paste a suspicious message to get it checked for red flags.",
        "home_scams_cta": "Check for scams",
        "home_for_kids": "Ask a Loved One",
        "home_for_kids_desc": "Turn something you learned, or a scam check result, into a short message you can share with family.",
        "home_for_kids_cta": "Create a message",
        "home_chat": "Ask a Question",
        "home_chat_desc": "Ask anything, in your own words. Answers stick to known facts and lay out options — never advice telling you what to do.",
        "home_chat_cta": "Start asking",
        "home_faq": "Common Questions",
        "home_faq_desc": "Real questions other people ask, on topics like debt, retirement, and saving — answered plainly.",
        "home_faq_cta": "See common questions",
        "home_kids_investing": "Investing in My Kids",
        "home_kids_investing_desc": "Ways to save or invest for a child's future, like 529 plans and custodial accounts, explained plainly.",
        "home_kids_investing_cta": "See the options",
        "kids_investing_title": "Investing in My Kids",
        "kids_investing_intro": "Ways to save or invest on behalf of a child — tap one to see a plain-language explanation.",
        "faq_title": "Common Questions",
        "faq_intro": "Questions people ask us often. No question is too basic — tap one to see a plain-language answer.",
        "select_topic": "Pick a topic to get a plain-language explanation.",
        "category": "Category",
        "subtopic": "Sub-topic",
        "explain": "Explain this",
        "misconceptions_intro": "Tap a statement to see if it's true, false, or somewhere in between.",
        "common_scams_intro": "Scammers often target older adults with urgent phone calls, fake tech support pop-ups, romance scams, and messages pretending to be from the government, a bank, or a grandchild in trouble. When in doubt, hang up or don't reply, then contact the organization directly using a number you look up yourself.",
        "scam_checker": "Scam-Checker",
        "scam_instructions": "Paste a suspicious text, email, or call transcript below.",
        "check_this": "Check this",
        "for_kids_title": "Ask a Loved One",
        "for_kids_prompt": "Turn something you learned, or a scam check result, into a short message you can text or email your family.",
        "for_kids_trust_note": "Ask someone you trust.",
        "for_kids_context": "What is this about?",
        "for_kids_recipient": "Who is this for?",
        "for_kids_recipient_placeholder": "e.g. my daughter Sarah, my son, a close friend",
        "for_kids_details": "Paste the explanation or details here",
        "for_kids_button": "Create message",
        "chat_title": "Ask a Question",
        "chat_prompt": "Welcome! What financial question is on your mind? Feel free to describe your own situation too (e.g. your age range, employment, or goals) so the answer can be more relevant — ask in your own words. I’ll share clear, factual information, explain options, and include links to trusted sources when I can. I won’t tell you what to do, and I’ll say when I’m unsure. For current numbers or rules, check the linked official source or speak with a licensed financial advisor.",
        "chat_placeholder": "Type your question here...",
        "send": "Send",
        "enter_message": "Paste a message above first.",
        "language": "Language",
    },
    "es": {
        "nav_home": "Inicio",
        "nav_101s": "101s",
        "nav_misconceptions": "Mitos",
        "nav_scams": "Estafas Comunes",
        "nav_for_kids": "Preguntarle a un ser querido",
        "nav_kids_investing": "Invertir en mis hijos",
        "nav_chat": "Haz una pregunta",
        "nav_faq": "Preguntas frecuentes",
        "welcome": "Bienvenido",
        "welcome_text": "FINtellect te ayuda a ganar confianza financiera a tu ritmo. Es gratis, no necesitas cuenta ni hay analítica ni revisores humanos: lo que escribes solo se envía al modelo de IA para generar tu respuesta.",
        "home_101s": "101s",
        "home_101s_desc": "Guías en lenguaje claro sobre jubilación, préstamos, ahorro, Seguridad Social, Medicare, planificación patrimonial, seguros e inversiones.",
        "home_101s_cta": "Ver los 101s",
        "home_myths": "Mitos",
        "home_myths_desc": "Mira los mitos financieros comunes explicados: qué es cierto y qué no.",
        "home_myths_cta": "Revisar un mito",
        "home_scams": "Estafas Comunes",
        "home_scams_desc": "Aprende sobre estafas frecuentes y pega un mensaje sospechoso para revisarlo.",
        "home_scams_cta": "Revisar estafas",
        "home_for_kids": "Preguntarle a un ser querido",
        "home_for_kids_desc": "Convierte algo que aprendiste o un resultado de una estafa en un mensaje breve para compartir con tu familia.",
        "home_for_kids_cta": "Crear un mensaje",
        "home_chat": "Haz una pregunta",
        "home_chat_desc": "Pregunta cualquier cosa con tus palabras. Las respuestas se basan en hechos y presentan opciones, nunca un consejo directo.",
        "home_chat_cta": "Empezar",
        "home_faq": "Preguntas frecuentes",
        "home_faq_desc": "Preguntas reales de otras personas sobre deudas, jubilación y ahorro, respondidas con claridad.",
        "home_faq_cta": "Ver preguntas frecuentes",
        "home_kids_investing": "Invertir en mis hijos",
        "home_kids_investing_desc": "Formas de ahorrar o invertir para el futuro de un niño, como planes 529 y cuentas de custodia, explicadas con claridad.",
        "home_kids_investing_cta": "Ver las opciones",
        "kids_investing_title": "Invertir en mis hijos",
        "kids_investing_intro": "Formas de ahorrar o invertir en nombre de un niño: toca una para ver una explicación clara.",
        "faq_title": "Preguntas frecuentes",
        "faq_intro": "Preguntas que nos hacen a menudo. Ninguna pregunta es demasiado básica: toca una para ver una respuesta clara.",
        "select_topic": "Elige un tema para obtener una explicación clara.",
        "category": "Categoría",
        "subtopic": "Subtema",
        "explain": "Explicar",
        "misconceptions_intro": "Toca una afirmación para ver si es verdadera, falsa o algo intermedio.",
        "common_scams_intro": "Los estafadores suelen dirigirse a personas mayores con llamadas urgentes, avisos falsos de soporte técnico, estafas románticas y mensajes que parecen venir de un gobierno, banco o nieto en problemas. Si dudas, cuelga o no contestes y contacta directamente con la organización usando un número que revises por tu cuenta.",
        "scam_checker": "Comprobador de estafas",
        "scam_instructions": "Pega un texto sospechoso, correo o transcripción de una llamada.",
        "check_this": "Comprobar",
        "for_kids_title": "Preguntarle a un ser querido",
        "for_kids_prompt": "Convierte algo que aprendiste o el resultado de una revisión de estafa en un mensaje breve para enviar por texto o correo.",
        "for_kids_trust_note": "Pregúntale a alguien de confianza.",
        "for_kids_context": "¿De qué trata?",
        "for_kids_recipient": "¿Para quién es esto?",
        "for_kids_recipient_placeholder": "p. ej. mi hija Sara, mi hijo, un amigo cercano",
        "for_kids_details": "Pega la explicación o los detalles aquí",
        "for_kids_button": "Crear mensaje",
        "chat_title": "Haz una pregunta",
        "chat_prompt": "¡Bienvenido! ¿Qué pregunta financiera tienes? Si quieres, describe también tu situación (edad, trabajo, metas) para una respuesta más útil — escríbela con tus propias palabras. Te compartiré información clara y basada en hechos, explicaré las opciones e incluiré enlaces a fuentes confiables cuando sea posible. No te diré qué debes hacer y te avisaré si no estoy segura. Para confirmar cifras o reglas actuales, consulta la fuente oficial enlazada o a un asesor financiero autorizado.",
        "chat_placeholder": "Escribe tu pregunta aquí...",
        "send": "Enviar",
        "enter_message": "Pega un mensaje arriba primero.",
        "language": "Idioma",
    },
    "fr": {
        "nav_home": "Accueil",
        "nav_101s": "101s",
        "nav_misconceptions": "Idées fausses",
        "nav_scams": "Arnaques courantes",
        "nav_for_kids": "Demander à un proche",
        "nav_kids_investing": "Investir pour mes enfants",
        "nav_chat": "Poser une question",
        "nav_faq": "Questions fréquentes",
        "welcome": "Bienvenue",
        "welcome_text": "FINtellect vous aide à gagner en confiance financière à votre rythme. Gratuit, sans compte, sans analyse ni relecteurs humains — ce que vous tapez est envoyé uniquement au modèle IA pour générer votre réponse.",
        "home_101s": "101s",
        "home_101s_desc": "Guides en langage simple sur la retraite, les prêts, l'épargne, la Sécurité sociale, Medicare, la planification successorale, l'assurance et l'investissement.",
        "home_101s_cta": "Voir les 101s",
        "home_myths": "Idées fausses",
        "home_myths_desc": "Découvrez les mythes courants sur l'argent expliqués simplement.",
        "home_myths_cta": "Vérifier un mythe",
        "home_scams": "Arnaques courantes",
        "home_scams_desc": "Apprenez les arnaques fréquentes et collez un message suspect pour le vérifier.",
        "home_scams_cta": "Vérifier une arnaque",
        "home_for_kids": "Demander à un proche",
        "home_for_kids_desc": "Transformez ce que vous avez appris, ou un résultat d'analyse d'arnaque, en un message simple à partager avec votre famille.",
        "home_for_kids_cta": "Créer un message",
        "home_chat": "Poser une question",
        "home_chat_desc": "Posez n'importe quelle question avec vos mots. Les réponses s'appuient sur des faits et présentent des options, sans conseil direct.",
        "home_chat_cta": "Commencer",
        "home_faq": "Questions fréquentes",
        "home_faq_desc": "De vraies questions sur la dette, la retraite et l'épargne, expliquées simplement.",
        "home_faq_cta": "Voir les questions fréquentes",
        "home_kids_investing": "Investir pour mes enfants",
        "home_kids_investing_desc": "Des façons d'épargner ou d'investir pour l'avenir d'un enfant, comme les plans 529 et les comptes de garde, expliquées simplement.",
        "home_kids_investing_cta": "Voir les options",
        "kids_investing_title": "Investir pour mes enfants",
        "kids_investing_intro": "Des façons d'épargner ou d'investir au nom d'un enfant — touchez-en une pour voir une explication claire.",
        "faq_title": "Questions fréquentes",
        "faq_intro": "Des questions qu'on nous pose souvent. Aucune question n'est trop simple — touchez-en une pour voir une réponse claire.",
        "select_topic": "Choisissez un sujet pour obtenir une explication simple.",
        "category": "Catégorie",
        "subtopic": "Sous-thème",
        "explain": "Expliquer",
        "misconceptions_intro": "Touchez une affirmation pour savoir si elle est vraie, fausse ou quelque part entre les deux.",
        "common_scams_intro": "Les arnaqueurs ciblent souvent les personnes âgées avec des appels urgents, des faux messages de support technique, des arnaques sentimentales et des messages prétendant venir du gouvernement, d'une banque ou d'un petit-enfant en difficulté. En cas de doute, raccrochez ou ne répondez pas, puis contactez directement l'organisation en utilisant un numéro que vous aurez vérifié vous-même.",
        "scam_checker": "Vérificateur d'arnaque",
        "scam_instructions": "Collez un texte suspect, un e-mail ou une transcription d'appel.",
        "check_this": "Vérifier",
        "for_kids_title": "Demander à un proche",
        "for_kids_prompt": "Transformez ce que vous avez appris, ou un résultat d'analyse d'arnaque, en un message court à envoyer par SMS ou e-mail.",
        "for_kids_trust_note": "Demandez à quelqu'un de confiance.",
        "for_kids_context": "De quoi s'agit-il ?",
        "for_kids_recipient": "Pour qui est-ce ?",
        "for_kids_recipient_placeholder": "ex. ma fille Sarah, mon fils, un ami proche",
        "for_kids_details": "Collez l'explication ou les détails ici",
        "for_kids_button": "Créer un message",
        "chat_title": "Poser une question",
        "chat_prompt": "Bienvenue ! Quelle question financière vous préoccupe ? Décrivez aussi votre situation si vous le souhaitez (âge, emploi, objectifs) pour une réponse plus pertinente — posez-la avec vos propres mots. Je vous donnerai des informations claires et factuelles, présenterai les options et ajouterai des liens vers des sources fiables lorsque possible. Je ne vous dirai pas quoi faire et je préciserai mes incertitudes. Pour vérifier les chiffres ou règles à jour, consultez la source officielle indiquée ou un conseiller financier agréé.",
        "chat_placeholder": "Saisissez votre question ici...",
        "send": "Envoyer",
        "enter_message": "Collez d'abord un message ci-dessus.",
        "language": "Langue",
    },
    "de": {
        "nav_home": "Startseite",
        "nav_101s": "101s",
        "nav_misconceptions": "Mythen",
        "nav_scams": "Häufige Betrugsfälle",
        "nav_for_kids": "Einen Angehörigen fragen",
        "nav_kids_investing": "In meine Kinder investieren",
        "nav_chat": "Frage stellen",
        "nav_faq": "Häufige Fragen",
        "welcome": "Willkommen",
        "welcome_text": "FINtellect hilft Ihnen, im eigenen Tempo mehr finanzielles Selbstvertrauen zu gewinnen. Kostenlos, ohne Konto, ohne Analyse oder menschliche Prüfer — Ihre Eingaben werden nur an das KI-Modell gesendet, um Ihre Antwort zu erzeugen.",
        "home_101s": "101s",
        "home_101s_desc": "Einfachsprachige Erläuterungen zu Rente, Krediten, Sparen, Sozialversicherung, Medicare, Nachlassplanung, Versicherung und Investitionen.",
        "home_101s_cta": "101s ansehen",
        "home_myths": "Mythen",
        "home_myths_desc": "Sehen Sie verbreitete Geldmythen erklärt — was stimmt und was nicht.",
        "home_myths_cta": "Mythos prüfen",
        "home_scams": "Häufige Betrugsfälle",
        "home_scams_desc": "Erfahren Sie mehr über häufige Betrugsmuster und fügen Sie eine verdächtige Nachricht ein, um sie prüfen zu lassen.",
        "home_scams_cta": "Betrug prüfen",
        "home_for_kids": "Einen Angehörigen fragen",
        "home_for_kids_desc": "Machen Sie aus etwas, das Sie gelernt haben, oder aus einem Betrugscheck-Ergebnis eine kurze Nachricht für Ihre Familie.",
        "home_for_kids_cta": "Nachricht erstellen",
        "home_chat": "Frage stellen",
        "home_chat_desc": "Stellen Sie alles in Ihren eigenen Worten. Antworten basieren auf Fakten und zeigen Optionen, ohne direkt zu beraten.",
        "home_chat_cta": "Loslegen",
        "home_faq": "Häufige Fragen",
        "home_faq_desc": "Echte Fragen zu Schulden, Rente und Sparen — einfach erklärt.",
        "home_faq_cta": "Häufige Fragen ansehen",
        "home_kids_investing": "In meine Kinder investieren",
        "home_kids_investing_desc": "Möglichkeiten, für die Zukunft eines Kindes zu sparen oder zu investieren, wie 529-Pläne und Verwahrkonten, einfach erklärt.",
        "home_kids_investing_cta": "Optionen ansehen",
        "kids_investing_title": "In meine Kinder investieren",
        "kids_investing_intro": "Möglichkeiten, im Namen eines Kindes zu sparen oder zu investieren — tippen Sie auf eine, um eine klare Erklärung zu sehen.",
        "faq_title": "Häufige Fragen",
        "faq_intro": "Fragen, die uns oft gestellt werden. Keine Frage ist zu einfach — tippen Sie auf eine, um eine klare Antwort zu sehen.",
        "select_topic": "Wählen Sie ein Thema für eine leicht verständliche Erklärung.",
        "category": "Kategorie",
        "subtopic": "Unterthema",
        "explain": "Erklären",
        "misconceptions_intro": "Tippen Sie auf eine Aussage, um zu sehen, ob sie wahr, falsch oder irgendwo dazwischen ist.",
        "common_scams_intro": "Betrüger zielen oft auf ältere Erwachsene mit Dringlichkeitsaufforderungen, gefälschten Tech-Support-Meldungen, Liebesbetrug und Nachrichten ab, die so tun, als kämen sie von der Regierung, einer Bank oder einem Enkelkind in Schwierigkeiten. Wenn Sie unsicher sind, legen Sie auf oder antworten Sie nicht und kontaktieren Sie die Organisation direkt über eine Nummer, die Sie selbst nachschlagen.",
        "scam_checker": "Betrugsprüfer",
        "scam_instructions": "Fügen Sie einen verdächtigen Text, eine E-Mail oder eine Gesprächstranskription ein.",
        "check_this": "Prüfen",
        "for_kids_title": "Einen Angehörigen fragen",
        "for_kids_prompt": "Machen Sie aus dem, was Sie gelernt haben, oder aus dem Ergebnis eines Betrugschecks eine kurze Nachricht für SMS oder E-Mail.",
        "for_kids_trust_note": "Fragen Sie jemanden, dem Sie vertrauen.",
        "for_kids_context": "Worum geht es?",
        "for_kids_recipient": "Für wen ist das?",
        "for_kids_recipient_placeholder": "z. B. meine Tochter Sarah, mein Sohn, ein guter Freund",
        "for_kids_details": "Fügen Sie die Erklärung oder Details hier ein",
        "for_kids_button": "Nachricht erstellen",
        "chat_title": "Frage stellen",
        "chat_prompt": "Willkommen! Welche Finanzfrage beschäftigt Sie? Beschreiben Sie gerne auch Ihre Situation (Alter, Beschäftigung, Ziele) für eine passendere Antwort — stellen Sie Ihre Frage einfach in Ihren eigenen Worten. Ich teile klare, sachliche Informationen und erläutere Optionen, ohne Ihnen vorzuschreiben, was Sie tun sollen. Wenn ich unsicher bin, sage ich es offen. Aktuelle Zahlen oder Regeln prüfen Sie bitte bei einer offiziellen Quelle oder einer qualifizierten Finanzberatung.",
        "chat_placeholder": "Geben Sie Ihre Frage ein und drücken Sie Enter...",
        "send": "Senden",
        "enter_message": "Fügen Sie zuerst eine Nachricht oben ein.",
        "language": "Sprache",
    },
}

HOME_HERO_TEXT = {
    "en": (
        "Build financial confidence for every chapter of life",
        "FINtellect exists to help people later in life gain financial literacy through plain-language guidance, scam protection, and personalized education for everyday decisions.",
    ),
    "es": (
        "Fortalece tu confianza financiera en cada etapa de la vida",
        "FINtellect ayuda a las personas en etapas avanzadas de la vida a desarrollar conocimientos financieros mediante orientación clara, protección contra estafas y educación personalizada para las decisiones cotidianas.",
    ),
    "fr": (
        "Renforcez votre confiance financière à chaque étape de la vie",
        "FINtellect aide les personnes plus âgées à acquérir des connaissances financières grâce à des explications claires, à la prévention des escroqueries et à une éducation personnalisée pour les décisions du quotidien.",
    ),
    "de": (
        "Finanzielle Sicherheit in jeder Lebensphase stärken",
        "FINtellect unterstützt ältere Menschen dabei, Finanzwissen aufzubauen – mit verständlicher Orientierung, Schutz vor Betrug und persönlicher Bildung für alltägliche Entscheidungen.",
    ),
    "it": (
        "Rafforza la tua sicurezza finanziaria in ogni fase della vita",
        "FINtellect aiuta le persone in età avanzata a sviluppare competenze finanziarie con indicazioni chiare, protezione dalle truffe e formazione personalizzata per le decisioni di ogni giorno.",
    ),
    "pt": (
        "Fortaleça sua confiança financeira em todas as fases da vida",
        "A FINtellect ajuda pessoas em fases mais avançadas da vida a desenvolver conhecimentos financeiros com orientações claras, proteção contra golpes e educação personalizada para decisões do dia a dia.",
    ),
    "zh-cn": (
        "在人生每个阶段建立财务信心",
        "FINtellect 通过通俗易懂的指导、防诈骗帮助和个性化教育，帮助年长人士提升金融知识，更从容地应对日常财务决策。",
    ),
    "ja": (
        "人生のあらゆる段階で、金融への自信を育てる",
        "FINtellectは、わかりやすい案内、詐欺から身を守るための情報、日々の判断に役立つ個別の学習を通じて、年齢を重ねた方の金融リテラシー向上を支援します。",
    ),
    "ko": (
        "삶의 모든 시기에 금융 자신감을 키우세요",
        "FINtellect는 이해하기 쉬운 안내, 사기 예방 정보, 일상적인 결정을 위한 맞춤형 교육을 통해 중장년층의 금융 이해력 향상을 돕습니다.",
    ),
    "ar": (
        "عزّز ثقتك المالية في كل مرحلة من مراحل الحياة",
        "تساعد FINtellect الأشخاص في مراحل لاحقة من الحياة على اكتساب المعرفة المالية من خلال إرشادات واضحة، ومعلومات للحماية من الاحتيال، وتثقيف مخصص للقرارات اليومية.",
    ),
    "hi": (
        "जीवन के हर पड़ाव पर वित्तीय आत्मविश्वास बढ़ाएँ",
        "FINtellect आसान भाषा में मार्गदर्शन, धोखाधड़ी से बचाव की जानकारी और रोज़मर्रा के फैसलों के लिए व्यक्तिगत शिक्षा देकर अधिक उम्र के लोगों की वित्तीय समझ बढ़ाने में मदद करता है।",
    ),
    "ru": (
        "Уверенность в финансовых вопросах на каждом этапе жизни",
        "FINtellect помогает людям старшего возраста развивать финансовую грамотность благодаря понятным рекомендациям, информации о защите от мошенничества и персональному обучению для повседневных решений.",
    ),
    "tr": (
        "Hayatın her döneminde finansal güveninizi güçlendirin",
        "FINtellect, ileri yaştaki kişilerin finansal okuryazarlığını sade anlatımlı rehberlik, dolandırıcılığa karşı korunma bilgileri ve günlük kararlar için kişiselleştirilmiş eğitimle destekler.",
    ),
    "pl": (
        "Buduj pewność finansową na każdym etapie życia",
        "FINtellect pomaga osobom na późniejszym etapie życia rozwijać wiedzę finansową dzięki jasnym wskazówkom, ochronie przed oszustwami i dopasowanej edukacji dotyczącej codziennych decyzji.",
    ),
    "uk": (
        "Зміцнюйте фінансову впевненість на кожному етапі життя",
        "FINtellect допомагає людям старшого віку здобувати фінансові знання завдяки зрозумілим порадам, інформації про захист від шахрайства та персоналізованій освіті для щоденних рішень.",
    ),
    "vi": (
        "Xây dựng sự tự tin về tài chính ở mọi giai đoạn cuộc đời",
        "FINtellect giúp người lớn tuổi nâng cao hiểu biết tài chính thông qua hướng dẫn dễ hiểu, thông tin phòng tránh lừa đảo và nội dung giáo dục phù hợp với các quyết định hằng ngày.",
    ),
    "nl": (
        "Bouw financieel vertrouwen op in elke levensfase",
        "FINtellect helpt mensen op latere leeftijd hun financiële kennis te vergroten met duidelijke uitleg, bescherming tegen oplichting en persoonlijke voorlichting voor dagelijkse beslissingen.",
    ),
    "sw": (
        "Jenga ujasiri wa kifedha katika kila hatua ya maisha",
        "FINtellect huwasaidia watu walio katika hatua za baadaye za maisha kujifunza kuhusu fedha kupitia maelezo rahisi, mwongozo wa kujilinda dhidi ya ulaghai na elimu inayolingana na maamuzi ya kila siku.",
    ),
    "id": (
        "Bangun kepercayaan diri finansial di setiap tahap kehidupan",
        "FINtellect membantu orang di usia lanjut meningkatkan literasi keuangan melalui panduan yang mudah dipahami, perlindungan dari penipuan, dan edukasi yang disesuaikan untuk keputusan sehari-hari.",
    ),
    "bn": (
        "জীবনের প্রতিটি পর্যায়ে আর্থিক আত্মবিশ্বাস গড়ে তুলুন",
        "FINtellect সহজ ভাষার দিকনির্দেশনা, প্রতারণা থেকে সুরক্ষার তথ্য এবং দৈনন্দিন সিদ্ধান্তের জন্য ব্যক্তিগত শিক্ষার মাধ্যমে বয়স্কদের আর্থিক জ্ঞান বাড়াতে সহায়তা করে।",
    ),
}


def t(lang, key):
    return UI_TEXT.get(lang or "en", UI_TEXT["en"]).get(key, UI_TEXT["en"][key])


def hero_text(lang):
    return HOME_HERO_TEXT.get(lang or "en", HOME_HERO_TEXT["en"])


def navigation_options(lang):
    return [
        {"label": t(lang, label_key), "value": tab_value}
        for label_key, tab_value in [
            ("nav_home", "tab-home"),
            ("nav_101s", "tab-101s"),
            ("nav_misconceptions", "tab-misconceptions"),
            ("nav_faq", "tab-faq"),
            ("nav_scams", "tab-scams"),
            ("nav_for_kids", "tab-for-kids"),
            ("nav_kids_investing", "tab-kids-investing"),
            ("nav_chat", "tab-chat"),
        ]
    ]


def error_card(exc):
    return html.Div(
        [
            html.P(
                "We couldn't get a response just now (the request failed or "
                "was blocked by a safety filter). If you're checking a "
                "message you think might be a scam, treat it as suspicious: "
                "don't reply or click any links, and contact the "
                "organization directly using a number you look up yourself."
            ),
            html.P(str(exc), className="token-note"),
        ],
        className="result-card risk-high",
    )


def share_button(section_id):
    return html.P(
        [
            "To turn this into a message for your family, open the ",
            html.Strong("Ask a Loved One"),
            " tab above — it will be pre-filled.",
        ],
        className="token-note",
    )


PROFILE_DEFAULTS = {
    "age": 58,
    "city": "Springfield",
    "state": "IL",
    "filing_status": "Single",
    "children_count": 3,
    "savings_balance": 2000,
    "savings_provider": "Marcus by Goldman Sachs",
    "retirement_401k_balance": 10000,
    "retirement_401k_provider": "Fidelity",
    "retirement_goal_age": 65,
    "annual_income": 62000,
    "income_history": {
        "2022": 54000,
        "2023": 57000,
        "2024": 59000,
        "2025": 61000,
        "2026": 62000,
    },
    "contact_1_name": "Sarah Johnson",
    "contact_1_relationship": "Daughter",
    "contact_1_phone": "(555) 123-4567",
    "contact_2_name": "Mike Chen",
    "contact_2_relationship": "Close friend",
    "contact_2_phone": "(555) 987-6543",
    "linked_accounts": [],
}

CREDIT_CARDS = [
    {
        "name": "Chase Sapphire Preferred",
        "points": 45000,
        "unit": "points",
        "options": [
            {"label": "Cash back / statement credit", "rate": 0.01},
            {"label": "Flights (travel portal)", "rate": 0.0125},
            {"label": "Hotels (travel portal)", "rate": 0.01},
            {"label": "Gift cards", "rate": 0.009},
        ],
    },
    {
        "name": "Capital One Venture Rewards",
        "points": 28000,
        "unit": "miles",
        "options": [
            {"label": "Cash back / erase travel purchase", "rate": 0.01},
            {"label": "Flights (erase travel purchase)", "rate": 0.01},
            {"label": "Hotels (travel portal)", "rate": 0.01},
            {"label": "Gift cards", "rate": 0.008},
        ],
    },
]


def compute_savings_target(profile):
    """Traditional retirement-calculator estimate: project current income to the
    goal age (3%/year average raises), assume 80% income replacement in
    retirement, then apply the standard 4%-withdrawal-rule 25x multiplier."""
    years_to_goal = max(int(profile["retirement_goal_age"]) - int(profile["age"]), 0)
    projected_income = float(profile["annual_income"]) * (1.03 ** years_to_goal)
    desired_retirement_income = projected_income * 0.8
    return desired_retirement_income * 25


def compute_shortfall_estimate(profile):
    """Demo-only projection: current savings + 401(k) grown at 5%/year
    until the retirement goal age, compared against the savings target."""
    years = max(int(profile["retirement_goal_age"]) - int(profile["age"]), 0)
    current_total = float(profile["savings_balance"]) + float(profile["retirement_401k_balance"])
    projected = current_total * (1.05 ** years)
    savings_target = compute_savings_target(profile)
    shortfall = max(savings_target - projected, 0)
    return years, current_total, shortfall, savings_target


def build_income_figure(income_history):
    years = sorted(income_history.keys())
    values = [income_history[y] for y in years]
    return {
        "data": [
            {
                "type": "scatter",
                "mode": "lines+markers",
                "x": years,
                "y": values,
                "line": {"color": "#4c8c82", "width": 3},
                "marker": {"color": "#4c8c82", "size": 8},
                "hovertemplate": "%{x}: $%{y:,.0f}<extra></extra>",
            }
        ],
        "layout": {
            "margin": {"l": 56, "r": 16, "t": 16, "b": 36},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "yaxis": {"title": "Annual income ($)", "tickformat": "$,.0f"},
            "xaxis": {"title": "Year", "type": "category"},
            "font": {"family": "-apple-system, Helvetica, Arial, sans-serif", "size": 13},
            "height": 280,
        },
    }


def render_linked_accounts(accounts):
    rows = []
    for i, account in enumerate(accounts or []):
        rows.append(
            html.Div(
                [
                    html.Label("Account name"),
                    dcc.Input(
                        id={"type": "linked-account-name", "index": i},
                        type="text",
                        value=account.get("name", ""),
                        className="text-field",
                    ),
                ],
                className="profile-field",
            )
        )
        rows.append(
            html.Div(
                [
                    html.Label("Balance ($)"),
                    dcc.Input(
                        id={"type": "linked-account-balance", "index": i},
                        type="number",
                        value=account.get("balance", 0),
                        className="text-field",
                    ),
                ],
                className="profile-field",
            )
        )
    return rows


def render_credit_card_rewards(open_card=None):
    items = []
    for i, card in enumerate(CREDIT_CARDS):
        cash_value = card["points"] * 0.01
        is_open = open_card == i
        items.append(
            html.Div(
                [
                    html.P(f"{card['name']} · {card['points']:,} {card['unit']}"),
                    html.Strong(f"≈ ${cash_value:,.0f} cash value"),
                    html.Button(
                        "Hide redemption options" if is_open else "See redemption options",
                        id={"type": "redeem-toggle", "index": i},
                        className="secondary-button profile-redeem-toggle",
                        n_clicks=0,
                    ),
                ],
                className="profile-stat",
            )
        )
        if is_open:
            items.append(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span(opt["label"]),
                                html.Strong(f"≈ ${card['points'] * opt['rate']:,.0f}"),
                            ],
                            className="profile-redeem-option",
                        )
                        for opt in card["options"]
                    ],
                    className="profile-redeem-panel",
                )
            )
    return items


# ---------- Layout ----------

app.layout = html.Div(
    [
        html.Div(
            "For demo purposes only",
            className="demo-disclaimer",
            role="note",
        ),
        html.Div(
            [html.Div(className="top-papel-flag") for _ in range(7)],
            className="top-papel-banner",
            role="presentation",
        ),
        html.Div(
            [
                html.Button(
                    html.Span(
                        [html.Span(), html.Span(), html.Span()],
                        className="menu-icon",
                    ),
                    id="menu-toggle",
                    className="menu-toggle",
                    type="button",
                    title="Toggle section menu",
                    **{"aria-label": "Toggle section menu"},
                ),
                html.Div(
                    [
                        html.Button(
                            "FINtellect",
                            id="wordmark-home",
                            className="wordmark",
                            type="button",
                            title="Go to Home",
                        ),
                    ],
                    className="header-brand",
                ),
                html.Div(
                    [
                        html.Button(
                            "?",
                            id="header-help",
                            className="header-help",
                            type="button",
                            title="Open help and chat",
                            **{"aria-label": "Open help and chat"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="language-picker",
                                    options=LANGUAGE_OPTIONS,
                                    value="en",
                                    clearable=False,
                                    searchable=True,
                                    className="language-picker",
                                    style={"minWidth": "150px", "width": "150px"},
                                ),
                                dcc.Store(id="language-store", data="en"),
                            ],
                            className="header-actions",
                        ),
                        html.Button(
                            t("en", "nav_profile"),
                            id="header-profile",
                            className="nav-signin",
                            type="button",
                        ),
                    ],
                    className="header-cta",
                ),
            ],
            className="app-header",
        ),
        html.Div(
            [
                html.Aside(
                    [
                        html.Div("Explore", className="section-picker-heading"),
                        dcc.RadioItems(
                            id="main-tabs",
                            options=navigation_options("en"),
                            value="tab-home",
                            className="section-picker",
                        ),
                    ],
                    className="sidebar-nav",
                    id="sidebar-nav",
                    role="navigation",
                    title="Main navigation",
                ),
                html.Div(id="tab-content", className="content-panel"),
                dcc.Store(id="last-result-store"),
                dcc.Store(id="chat-history-store", data=[]),
                dcc.Store(id="profile-store", data=PROFILE_DEFAULTS),
                dcc.Store(id="redeem-open-store", data=None),
            ],
            className="app-shell",
            id="app-shell",
        ),
        html.Button(
            "Chatbot",
            id="chatbot-shortcut",
            className="chatbot-shortcut",
            type="button",
            title="Open the chatbot",
        ),
    ]
)


# ---------- Tab content ----------

def render_home(lang):
    hero_title, mission_statement = hero_text(lang)
    cards = [
        html.Div(
            [
                html.H3(t(lang, title_key)),
                html.P(t(lang, desc_key)),
                html.Button(
                    t(lang, cta_key),
                    id={"type": "home-nav", "tab": tab_value},
                    className="secondary-button",
                ),
            ],
            className="home-card",
        )
        for tab_value, title_key, desc_key, cta_key in [
            ("tab-101s", "home_101s", "home_101s_desc", "home_101s_cta"),
            ("tab-misconceptions", "home_myths", "home_myths_desc", "home_myths_cta"),
            ("tab-faq", "home_faq", "home_faq_desc", "home_faq_cta"),
            ("tab-scams", "home_scams", "home_scams_desc", "home_scams_cta"),
            ("tab-for-kids", "home_for_kids", "home_for_kids_desc", "home_for_kids_cta"),
            ("tab-kids-investing", "home_kids_investing", "home_kids_investing_desc", "home_kids_investing_cta"),
            ("tab-chat", "home_chat", "home_chat_desc", "home_chat_cta"),
        ]
    ]
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(hero_title, className="hero-title"),
                            html.P(
                                mission_statement,
                                className="mission-statement",
                            ),
                        ],
                        className="hero-copy",
                    ),
                ],
                className="hero-shell",
            ),
            html.Div(
                [
                    html.Div(className="papel-banner papel-banner-left"),
                    html.Div(className="papel-banner papel-banner-center"),
                    html.Div(className="papel-banner papel-banner-right"),
                ],
                className="papel-banner-row",
            ),
            html.Div(cards, className="home-grid"),
        ],
        className="home-page",
    )


def render_101s(lang):
    return html.Div(
        [
            html.H2(t(lang, "nav_101s")),
            html.P(t(lang, "select_topic")),
            html.Label(t(lang, "category")),
            dcc.Dropdown(
                id="topic-category",
                options=[{"label": l, "value": s} for s, l in get_category_labels()],
                value=get_category_labels()[0][0],
                clearable=False,
            ),
            html.Label(t(lang, "subtopic")),
            dcc.Dropdown(id="topic-subtopic", clearable=False),
            html.Button(t(lang, "explain"), id="explain-topic-btn", className="primary-button"),
            dcc.Loading(html.Div(id="topic-result")),
        ]
    )


def render_misconception_items(open_slug=None, answer=None):
    items = []
    for slug, text in MISCONCEPTIONS:
        is_open = slug == open_slug
        items.append(
            html.Button(
                text,
                id={"type": "misconception-btn", "slug": slug},
                className="faq-question-open" if is_open else "",
            )
        )
        if is_open and answer is not None:
            items.append(answer)
    return items


def render_misconceptions(lang):
    return html.Div(
        [
            html.H2(t(lang, "nav_misconceptions")),
            html.P(t(lang, "misconceptions_intro")),
            dcc.Loading(
                html.Div(
                    render_misconception_items(),
                    id="misconception-list",
                    className="misconception-list",
                )
            ),
        ]
    )


def render_faq_items(open_slug=None, answer=None):
    items = []
    for slug, text in COMMON_QUESTIONS:
        is_open = slug == open_slug
        items.append(
            html.Button(
                text,
                id={"type": "faq-btn", "slug": slug},
                className="faq-question-open" if is_open else "",
            )
        )
        if is_open and answer is not None:
            items.append(answer)
    return items


def render_faq(lang):
    return html.Div(
        [
            html.H2(t(lang, "faq_title")),
            html.P(t(lang, "faq_intro")),
            dcc.Loading(
                html.Div(render_faq_items(), id="faq-list", className="misconception-list")
            ),
        ]
    )


def render_kids_investing_items(open_slug=None, answer=None):
    items = []
    for slug, text in KIDS_INVESTING_TOPICS:
        is_open = slug == open_slug
        items.append(
            html.Button(
                text,
                id={"type": "kids-investing-btn", "slug": slug},
                className="faq-question-open" if is_open else "",
            )
        )
        if is_open and answer is not None:
            items.append(answer)
    return items


def render_kids_investing(lang):
    return html.Div(
        [
            html.H2(t(lang, "kids_investing_title")),
            html.P(t(lang, "kids_investing_intro")),
            dcc.Loading(
                html.Div(
                    render_kids_investing_items(),
                    id="kids-investing-list",
                    className="misconception-list",
                )
            ),
        ]
    )


def render_scams(lang):
    return html.Div(
        [
            html.H2(t(lang, "nav_scams")),
            html.P(t(lang, "common_scams_intro")),
            html.H3("Common scam patterns"),
            html.Ul(
                [
                    html.Li([html.Strong(f"{title}: "), desc])
                    for title, desc in COMMON_SCAM_TYPES
                ],
                className="scam-reference-list",
            ),
            html.H3("Organizations scammers often impersonate"),
            html.P(
                "These are real, legitimate organizations — the scam is an "
                "unsolicited call, text, or email claiming to be them.",
                className="token-note",
            ),
            html.Ul(
                [
                    html.Li([html.Strong(f"{title}: "), desc])
                    for title, desc in ORGANIZATIONS_SCAMMERS_IMPERSONATE
                ],
                className="scam-reference-list",
            ),
            html.H2(t(lang, "scam_checker")),
            html.P(t(lang, "scam_instructions")),
            dcc.Textarea(id="scam-input", placeholder="Paste the message here..."),
            html.Button(t(lang, "check_this"), id="check-scam-btn", className="primary-button"),
            dcc.Loading(html.Div(id="scam-result")),
        ]
    )


def render_for_kids(lang, profile=None):
    profile = profile or PROFILE_DEFAULTS
    contact_options = [
        {
            "label": f"{profile['contact_1_name']} ({profile['contact_1_relationship']})",
            "value": "contact_1",
        },
        {
            "label": f"{profile['contact_2_name']} ({profile['contact_2_relationship']})",
            "value": "contact_2",
        },
    ]
    return html.Div(
        [
            html.H2(t(lang, "for_kids_title")),
            html.P(t(lang, "for_kids_prompt")),
            html.P(t(lang, "for_kids_trust_note"), className="token-note"),
            html.Label(t(lang, "for_kids_context")),
            dcc.Dropdown(
                id="kids-context",
                options=[
                    {"label": "A possible scam", "value": "A possible scam I encountered"},
                    {"label": "A retirement decision", "value": "A retirement decision I'm considering"},
                    {"label": "A general financial topic", "value": "A general financial topic I learned about"},
                ],
                value="A possible scam I encountered",
                clearable=False,
            ),
            html.Label(t(lang, "for_kids_recipient")),
            dcc.Dropdown(
                id="kids-recipient",
                options=contact_options,
                value="contact_1",
                clearable=False,
            ),
            html.P(
                "Texting uses the phone number saved for this contact on your "
                "Profile page.",
                className="token-note",
            ),
            html.Label(t(lang, "for_kids_details")),
            dcc.Textarea(id="kids-input", placeholder="Paste text from another section, or describe it yourself..."),
            html.Button(t(lang, "for_kids_button"), id="kids-btn", className="primary-button"),
            dcc.Loading(html.Div(id="kids-result")),
        ]
    )


def render_chat(lang):
    return html.Div(
        [
            html.H2(t(lang, "chat_title")),
            html.P(t(lang, "chat_prompt")),
            html.Div(id="chat-log", className="chat-log"),
            html.Div(
                [
                    dcc.Textarea(
                        id="chat-input",
                        placeholder=t(lang, "chat_placeholder"),
                        rows=4,
                        className="chat-text-input",
                    ),
                    html.Button(t(lang, "send"), id="chat-send-btn", className="primary-button"),
                ],
                className="chat-composer",
            ),
            dcc.Loading(html.Div(id="chat-loading-anchor")),
        ]
    )


def render_profile(lang, profile=None):
    profile = profile or PROFILE_DEFAULTS
    years, current_total, shortfall, savings_target = compute_shortfall_estimate(profile)
    income_history = profile["income_history"]
    income_year_inputs = [
        html.Div(
            [
                html.Label(year),
                dcc.Input(
                    id={"type": "profile-income-year", "year": year},
                    type="number",
                    value=income_history[year],
                    className="text-field profile-income-input",
                ),
            ],
            className="profile-income-year",
        )
        for year in sorted(income_history)
    ]
    return html.Div(
        [
            html.P("FICTIONAL DEMO PROFILE", className="profile-eyebrow"),
            html.H2("Demo Profile", className="profile-name"),
            html.P(
                "An illustrative example for exploring FINtellect. This is not a real person or a description of a typical family. Edit any field and press Save to see the numbers below update.",
                className="profile-intro",
            ),
            html.Section(
                [
                    html.H3("About"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Age"),
                                    dcc.Input(
                                        id="profile-age",
                                        type="number",
                                        value=profile["age"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.Label("City"),
                                    dcc.Input(
                                        id="profile-city",
                                        type="text",
                                        value=profile["city"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.Label("State"),
                                    dcc.Input(
                                        id="profile-state",
                                        type="text",
                                        value=profile["state"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.Label("Tax filing status"),
                                    dcc.Dropdown(
                                        id="profile-filing-status",
                                        options=[
                                            {"label": s, "value": s}
                                            for s in [
                                                "Single",
                                                "Married filing jointly",
                                                "Married filing separately",
                                                "Head of household",
                                            ]
                                        ],
                                        value=profile["filing_status"],
                                        clearable=False,
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.Label("Children"),
                                    dcc.Input(
                                        id="profile-children-count",
                                        type="number",
                                        value=profile["children_count"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                        ],
                        className="profile-field-grid",
                    ),
                ],
                className="profile-section",
            ),
            html.Section(
                [
                    html.H3("Annual income"),
                    html.Div(
                        [
                            html.Label("Current annual income ($)"),
                            dcc.Input(
                                id="profile-annual-income",
                                type="number",
                                value=profile["annual_income"],
                                className="text-field",
                            ),
                        ],
                        className="profile-field",
                    ),
                    html.Label("Past years (edit any year's income)", className="profile-income-history-label"),
                    html.Div(income_year_inputs, className="profile-income-year-row"),
                    dcc.Graph(
                        id="profile-income-graph",
                        figure=build_income_figure(income_history),
                        config={"displayModeBar": False},
                    ),
                ],
                className="profile-section",
            ),
            html.Section(
                [
                    html.H3("Financial snapshot"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(f"Savings · {profile['savings_provider']} ($)"),
                                    dcc.Input(
                                        id="profile-savings-balance",
                                        type="number",
                                        value=profile["savings_balance"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.Label(f"401(k) · {profile['retirement_401k_provider']} ($)"),
                                    dcc.Input(
                                        id="profile-401k-balance",
                                        type="number",
                                        value=profile["retirement_401k_balance"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                        ],
                        className="profile-field-grid",
                    ),
                    html.Div(
                        render_linked_accounts(profile.get("linked_accounts", [])),
                        id="linked-accounts-list",
                        className="profile-field-grid",
                    ),
                    html.P(
                        "Illustrative additional accounts only — this demo has no real bank "
                        "connection; it just adds another fictional line you can edit and save.",
                        className="profile-disclaimer",
                    ),
                    html.Div(
                        [
                            html.Button(
                                "+ Link new bank account",
                                id="add-bank-account-btn",
                                className="secondary-button",
                                n_clicks=0,
                            ),
                            html.Button(
                                "+ Link new savings account",
                                id="add-savings-account-btn",
                                className="secondary-button",
                                n_clicks=0,
                            ),
                            html.Button(
                                "+ Link new retirement account",
                                id="add-retirement-account-btn",
                                className="secondary-button",
                                n_clicks=0,
                            ),
                        ],
                        className="profile-link-account-buttons",
                    ),
                ],
                className="profile-section",
            ),
            html.Section(
                [
                    html.H3("Credit card rewards"),
                    html.Div(
                        render_credit_card_rewards(),
                        id="credit-card-rewards-list",
                        className="profile-stats",
                    ),
                    html.P(
                        "Estimated cash value only, assuming roughly 1¢ per point/mile "
                        "for a simple redemption. Actual value depends on the card's own "
                        "redemption options and terms, which vary by program and can change.",
                        className="profile-disclaimer",
                    ),
                ],
                className="profile-section",
            ),
            html.Section(
                [
                    html.H3("Goals"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Retirement goal age"),
                                    dcc.Input(
                                        id="profile-retirement-goal-age",
                                        type="number",
                                        value=profile["retirement_goal_age"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.P("Illustrative savings target"),
                                    html.Strong(
                                        f"${savings_target:,.0f}",
                                        id="profile-savings-target-value",
                                    ),
                                ],
                                className="profile-stat",
                            ),
                        ],
                        className="profile-field-grid",
                    ),
                    html.Div(
                        [
                            html.P("Estimated amount short"),
                            html.Strong(f"${shortfall:,.0f}", id="profile-shortfall-value"),
                        ],
                        className="profile-stat profile-stat-highlight",
                        id="profile-shortfall-stat",
                    ),
                    html.P(
                        f"Demo estimate only: the savings target uses a traditional retirement-calculator "
                        f"rule (projects your current income to your goal age at 3%/year raises, assumes you'll "
                        f"need 80% of that in retirement, then applies the standard 4%-withdrawal-rule 25x "
                        f"multiplier) and updates instantly as you change age, retirement goal age, or income. "
                        f"The amount-short estimate below assumes the current ${current_total:,.0f} grows by 5% "
                        f"annually for {years} years with no additional contributions, and updates when you "
                        "press Save. Illustrative only, not financial advice or a personalized projection.",
                        className="profile-disclaimer",
                        id="profile-estimate-note",
                    ),
                ],
                className="profile-section",
            ),
            html.Section(
                [
                    html.H3("Trusted contacts"),
                    html.P(
                        "People you could call to double-check something, or address an "
                        "“Ask a Loved One” message to.",
                        className="profile-disclaimer",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Name"),
                                    dcc.Input(
                                        id="profile-contact-1-name",
                                        type="text",
                                        value=profile["contact_1_name"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.Label("Relationship"),
                                    dcc.Input(
                                        id="profile-contact-1-relationship",
                                        type="text",
                                        value=profile["contact_1_relationship"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.Label("Phone"),
                                    dcc.Input(
                                        id="profile-contact-1-phone",
                                        type="text",
                                        value=profile["contact_1_phone"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                        ],
                        className="profile-field-grid",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Name"),
                                    dcc.Input(
                                        id="profile-contact-2-name",
                                        type="text",
                                        value=profile["contact_2_name"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.Label("Relationship"),
                                    dcc.Input(
                                        id="profile-contact-2-relationship",
                                        type="text",
                                        value=profile["contact_2_relationship"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                            html.Div(
                                [
                                    html.Label("Phone"),
                                    dcc.Input(
                                        id="profile-contact-2-phone",
                                        type="text",
                                        value=profile["contact_2_phone"],
                                        className="text-field",
                                    ),
                                ],
                                className="profile-field",
                            ),
                        ],
                        className="profile-field-grid",
                        style={"marginTop": "14px"},
                    ),
                ],
                className="profile-section",
            ),
            html.Section(
                [
                    html.H3("Family"),
                    html.Ul(
                        [html.Li(f"Child, age {age}") for age in (21, 22, 26)],
                        className="profile-family-list",
                    ),
                ],
                className="profile-section",
            ),
            html.Button("Save changes", id="profile-save-btn", className="primary-button"),
            html.P("", id="profile-save-status", className="token-note"),
            html.P(
                "All details are fictional and for demonstration only. Account provider names are examples, not endorsements.",
                className="profile-disclaimer",
            ),
        ],
        className="profile-page",
    )


def render_chat_log(history):
    bubbles = []
    for msg in history:
        if msg["role"] == "user":
            bubbles.append(html.Div(msg["content"], className="chat-bubble chat-bubble-user"))
        else:
            bubbles.append(
                dcc.Markdown(msg["content"], className="chat-bubble chat-bubble-assistant")
            )
    return bubbles


@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value"),
    Input("language-store", "data"),
    State("profile-store", "data"),
)
def render_tab(tab, lang, profile_data):
    lang = lang or "en"
    return {
        "tab-home": lambda: render_home(lang),
        "tab-101s": lambda: render_101s(lang),
        "tab-misconceptions": lambda: render_misconceptions(lang),
        "tab-faq": lambda: render_faq(lang),
        "tab-scams": lambda: render_scams(lang),
        "tab-for-kids": lambda: render_for_kids(lang, profile_data),
        "tab-kids-investing": lambda: render_kids_investing(lang),
        "tab-chat": lambda: render_chat(lang),
        "tab-profile": lambda: render_profile(lang, profile_data),
    }[tab]()


@app.callback(
    Output("main-tabs", "options"),
    Output("header-profile", "children"),
    Input("language-store", "data"),
)
def update_tabs(lang):
    lang = lang or "en"
    return navigation_options(lang), t(lang, "nav_profile")


# ---------- Language toggle ----------

@app.callback(
    Output("language-store", "data"),
    Input("language-picker", "value"),
    prevent_initial_call=True,
)
def update_language(selected_language):
    if not selected_language:
        raise PreventUpdate
    return selected_language


# ---------- Home navigation ----------

@app.callback(
    Output("main-tabs", "value"),
    Input({"type": "home-nav", "tab": ALL}, "n_clicks"),
    Input("wordmark-home", "n_clicks"),
    Input("chatbot-shortcut", "n_clicks"),
    Input("header-help", "n_clicks"),
    Input("header-profile", "n_clicks"),
    prevent_initial_call=True,
)
def navigate_from_home(
    n_clicks_list,
    wordmark_clicks,
    chatbot_clicks,
    help_clicks,
    profile_clicks,
):
    triggered = ctx.triggered_id
    if triggered == "wordmark-home":
        return "tab-home"
    if triggered in ("chatbot-shortcut", "header-help"):
        return "tab-chat"
    if triggered == "header-profile":
        return "tab-profile"
    if not triggered or not any(n_clicks_list):
        raise PreventUpdate
    return triggered["tab"]


@app.callback(
    Output("sidebar-nav", "className"),
    Output("app-shell", "className"),
    Input("menu-toggle", "n_clicks"),
    State("sidebar-nav", "className"),
    State("app-shell", "className"),
    prevent_initial_call=True,
)
def toggle_sidebar(menu_clicks, sidebar_class, shell_class):
    sidebar_class = sidebar_class or "sidebar-nav"
    shell_class = shell_class or "app-shell"
    if "is-collapsed" in sidebar_class:
        return (
            sidebar_class.replace(" is-collapsed", ""),
            shell_class.replace(" sidebar-collapsed", ""),
        )
    return f"{sidebar_class} is-collapsed", f"{shell_class} sidebar-collapsed"


@app.callback(
    Output("chatbot-shortcut", "className"),
    Input("main-tabs", "value"),
)
def toggle_chatbot_shortcut(tab):
    # Hidden on the chat tab itself, where it would sit on top of the
    # composer's Send button.
    if tab == "tab-chat":
        return "chatbot-shortcut chatbot-shortcut-hidden"
    return "chatbot-shortcut"


# ---------- 101s callbacks ----------

@app.callback(
    Output("topic-subtopic", "options"),
    Output("topic-subtopic", "value"),
    Input("topic-category", "value"),
)
def update_subtopics(category_slug):
    subtopics = get_subtopics(category_slug)
    options = [{"label": l, "value": s} for s, l in subtopics]
    return options, subtopics[0][0]


@app.callback(
    Output("topic-result", "children"),
    Output("last-result-store", "data"),
    Input("explain-topic-btn", "n_clicks"),
    State("topic-category", "value"),
    State("topic-subtopic", "value"),
    prevent_initial_call=True,
)
def explain_topic(n_clicks, category_slug, subtopic_slug):
    if not n_clicks:
        raise PreventUpdate
    category_label = TOPICS[category_slug]["label"]
    subtopic_label = get_subtopic_label(category_slug, subtopic_slug)
    try:
        text, usage = tutor_agent.explain_topic(category_label, subtopic_label)
    except AgentError as exc:
        return error_card(exc), None
    result = html.Div(
        [
            dcc.Markdown(text, className="result-card"),
            share_button("101s"),
        ]
    )
    return result, {"section": "A general financial topic I learned about", "text": text}


# ---------- Misconceptions callbacks ----------

@app.callback(
    Output("misconception-list", "children"),
    Output("last-result-store", "data", allow_duplicate=True),
    Input({"type": "misconception-btn", "slug": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def explain_misconception(n_clicks_list):
    triggered = ctx.triggered_id
    if not triggered or not any(n_clicks_list):
        raise PreventUpdate
    slug = triggered["slug"]
    misconception_text = get_misconception_label(slug)
    try:
        text, usage = tutor_agent.explain_misconception(misconception_text)
    except AgentError as exc:
        return render_misconception_items(slug, error_card(exc)), None
    answer = html.Div(
        [
            dcc.Markdown(text, className="result-card"),
            share_button("misconceptions"),
        ],
        className="faq-answer",
    )
    return render_misconception_items(slug, answer), {
        "section": "A general financial topic I learned about",
        "text": text,
    }


# ---------- Common Questions (FAQ) callbacks ----------

@app.callback(
    Output("faq-list", "children"),
    Output("last-result-store", "data", allow_duplicate=True),
    Input({"type": "faq-btn", "slug": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def answer_faq_question(n_clicks_list):
    triggered = ctx.triggered_id
    if not triggered or not any(n_clicks_list):
        raise PreventUpdate
    slug = triggered["slug"]
    question_text = get_question_label(slug)
    try:
        text, usage = tutor_agent.answer_faq(question_text)
    except AgentError as exc:
        return render_faq_items(slug, error_card(exc)), None
    answer = html.Div(
        [
            dcc.Markdown(text, className="result-card"),
            share_button("faq"),
        ],
        className="faq-answer",
    )
    return render_faq_items(slug, answer), {
        "section": "A general financial topic I learned about",
        "text": text,
    }


# ---------- Investing in My Kids callbacks ----------

@app.callback(
    Output("kids-investing-list", "children"),
    Output("last-result-store", "data", allow_duplicate=True),
    Input({"type": "kids-investing-btn", "slug": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def explain_kids_investing_topic(n_clicks_list):
    triggered = ctx.triggered_id
    if not triggered or not any(n_clicks_list):
        raise PreventUpdate
    slug = triggered["slug"]
    topic_label = get_kids_investing_label(slug)
    try:
        text, usage = tutor_agent.explain_kids_investing(topic_label)
    except AgentError as exc:
        return render_kids_investing_items(slug, error_card(exc)), None
    answer = html.Div(
        [
            dcc.Markdown(text, className="result-card"),
            share_button("kids-investing"),
        ],
        className="faq-answer",
    )
    return render_kids_investing_items(slug, answer), {
        "section": "A general financial topic I learned about",
        "text": text,
    }


# ---------- Scam-checker callbacks ----------

@app.callback(
    Output("scam-result", "children"),
    Output("last-result-store", "data", allow_duplicate=True),
    Input("check-scam-btn", "n_clicks"),
    State("scam-input", "value"),
    prevent_initial_call=True,
)
def check_scam(n_clicks, pasted_text):
    if not n_clicks:
        raise PreventUpdate
    if not pasted_text or not pasted_text.strip():
        return html.P("Paste a message above first."), None
    try:
        text, usage = scam_checker_agent.analyze(pasted_text)
    except AgentError as exc:
        return error_card(exc), None
    risk_class = "risk-low"
    if "RISK LEVEL: Medium" in text:
        risk_class = "risk-medium"
    elif "RISK LEVEL: High" in text:
        risk_class = "risk-high"
    result = html.Div(
        [
            dcc.Markdown(text, className=f"result-card {risk_class}"),
            share_button("scams"),
        ]
    )
    return result, {"section": "A possible scam I encountered", "text": text}


# ---------- Pre-fill Ask a Loved One tab from the last result, when opened ----------

@app.callback(
    Output("kids-input", "value"),
    Output("kids-context", "value"),
    Input("tab-content", "children"),
    State("main-tabs", "value"),
    State("last-result-store", "data"),
    prevent_initial_call=True,
)
def prefill_kids_tab(_tab_content, tab, stored):
    # Fires after render_tab has rebuilt tab-content, so kids-input/
    # kids-context are guaranteed to exist when this targets them.
    if tab != "tab-for-kids" or not stored:
        raise PreventUpdate
    return stored["text"], stored["section"]


# ---------- Ask a Loved One callback ----------

@app.callback(
    Output("kids-result", "children"),
    Input("kids-btn", "n_clicks"),
    State("kids-context", "value"),
    State("kids-recipient", "value"),
    State("kids-input", "value"),
    State("profile-store", "data"),
    prevent_initial_call=True,
)
def create_family_message(n_clicks, context_label, recipient_key, details, profile_data):
    if not n_clicks:
        raise PreventUpdate
    if not details or not details.strip():
        return html.P("Paste or describe the details above first.")
    profile = profile_data or PROFILE_DEFAULTS
    contact_name = profile.get(f"{recipient_key}_name", PROFILE_DEFAULTS[f"{recipient_key}_name"])
    contact_relationship = profile.get(
        f"{recipient_key}_relationship", PROFILE_DEFAULTS[f"{recipient_key}_relationship"]
    )
    contact_phone = profile.get(f"{recipient_key}_phone", PROFILE_DEFAULTS[f"{recipient_key}_phone"])
    recipient_label = f"{contact_name} ({contact_relationship})"
    try:
        text, usage = family_bridge_agent.summarize_for_family(context_label, details, recipient_label)
    except AgentError as exc:
        return error_card(exc)
    phone_digits = "".join(ch for ch in contact_phone if ch.isdigit() or ch == "+")
    sms_href = f"sms:{phone_digits}?&body=" + quote(text)
    return html.Div(
        [
            dcc.Markdown(text, className="result-card"),
            dcc.Textarea(value=text, style={"marginTop": "10px"}, id="kids-copy-box"),
            html.A(
                f"Text {contact_name}",
                href=sms_href,
                className="secondary-button",
                title="Opens your phone's own text message app, addressed to this saved contact, with this message filled in — you still have to tap send yourself.",
            ),
            html.P(
                "This only opens your own messaging app with the contact and text "
                "pre-filled — nothing is sent automatically. You still have to tap "
                "send yourself.",
                className="token-note",
            ),
        ]
    )


# ---------- Ask a Question (chat) ----------

@app.callback(
    Output("chat-log", "children"),
    Input("tab-content", "children"),
    State("main-tabs", "value"),
    State("chat-history-store", "data"),
    prevent_initial_call=True,
)
def populate_chat_log(_tab_content, tab, history):
    # Fires after render_tab rebuilds tab-content, so chat-log is
    # guaranteed to exist; restores the conversation when returning to
    # this tab (chat-history-store lives at the top level, so it
    # survives switching tabs, unlike tab-content's own children).
    if tab != "tab-chat":
        raise PreventUpdate
    return render_chat_log(history or [])


@app.callback(
    Output("chat-log", "children", allow_duplicate=True),
    Output("chat-history-store", "data"),
    Output("chat-input", "value"),
    Input("chat-send-btn", "n_clicks"),
    State("chat-input", "value"),
    State("chat-history-store", "data"),
    prevent_initial_call=True,
)
def handle_chat(n_clicks, message, history):
    if not n_clicks:
        raise PreventUpdate
    if not message or not message.strip():
        raise PreventUpdate
    history = history or []
    try:
        text, _usage = chat_agent.ask(history, message)
    except AgentError as exc:
        text = (
            "Sorry, I couldn't get an answer just now (the request failed "
            f"or was blocked by a safety filter: {exc}). Please try again, "
            "or check an official source directly."
        )
    new_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": text},
    ]
    return render_chat_log(new_history), new_history, ""


# ---------- Demo Profile (editable) ----------

@app.callback(
    Output("linked-accounts-list", "children"),
    Input("add-bank-account-btn", "n_clicks"),
    Input("add-savings-account-btn", "n_clicks"),
    Input("add-retirement-account-btn", "n_clicks"),
    State({"type": "linked-account-name", "index": ALL}, "value"),
    State({"type": "linked-account-balance", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def add_linked_account(bank_clicks, savings_clicks, retirement_clicks, names, balances):
    triggered = ctx.triggered_id
    if not triggered:
        raise PreventUpdate
    default_names = {
        "add-bank-account-btn": "New bank account",
        "add-savings-account-btn": "New savings account",
        "add-retirement-account-btn": "New retirement account",
    }
    if triggered not in default_names:
        raise PreventUpdate
    current_accounts = [
        {"name": name or "", "balance": balance if balance is not None else 0}
        for name, balance in zip(names, balances)
    ]
    current_accounts.append({"name": default_names[triggered], "balance": 0})
    return render_linked_accounts(current_accounts)


@app.callback(
    Output("credit-card-rewards-list", "children"),
    Output("redeem-open-store", "data"),
    Input({"type": "redeem-toggle", "index": ALL}, "n_clicks"),
    State("redeem-open-store", "data"),
    prevent_initial_call=True,
)
def toggle_redeem_options(n_clicks_list, open_card):
    triggered = ctx.triggered_id
    if not triggered or not any(n_clicks_list):
        raise PreventUpdate
    idx = triggered["index"]
    new_open = None if open_card == idx else idx
    return render_credit_card_rewards(new_open), new_open


@app.callback(
    Output("profile-savings-target-value", "children", allow_duplicate=True),
    Input("profile-age", "value"),
    Input("profile-retirement-goal-age", "value"),
    Input("profile-annual-income", "value"),
    prevent_initial_call=True,
)
def live_update_savings_target(age, goal_age, annual_income):
    if age is None or goal_age is None or annual_income is None:
        raise PreventUpdate
    target = compute_savings_target(
        {"age": age, "retirement_goal_age": goal_age, "annual_income": annual_income}
    )
    return f"${target:,.0f}"


@app.callback(
    Output("profile-store", "data"),
    Output("profile-save-status", "children"),
    Output("profile-shortfall-value", "children"),
    Output("profile-savings-target-value", "children"),
    Output("profile-estimate-note", "children"),
    Output("profile-income-graph", "figure"),
    Input("profile-save-btn", "n_clicks"),
    State("profile-age", "value"),
    State("profile-city", "value"),
    State("profile-state", "value"),
    State("profile-filing-status", "value"),
    State("profile-children-count", "value"),
    State("profile-savings-balance", "value"),
    State("profile-401k-balance", "value"),
    State("profile-retirement-goal-age", "value"),
    State("profile-annual-income", "value"),
    State({"type": "profile-income-year", "year": ALL}, "value"),
    State({"type": "profile-income-year", "year": ALL}, "id"),
    State("profile-contact-1-name", "value"),
    State("profile-contact-1-relationship", "value"),
    State("profile-contact-1-phone", "value"),
    State("profile-contact-2-name", "value"),
    State("profile-contact-2-relationship", "value"),
    State("profile-contact-2-phone", "value"),
    State({"type": "linked-account-name", "index": ALL}, "value"),
    State({"type": "linked-account-balance", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def save_profile(
    n_clicks,
    age,
    city,
    state,
    filing_status,
    children_count,
    savings_balance,
    k401_balance,
    goal_age,
    annual_income,
    income_values,
    income_ids,
    contact_1_name,
    contact_1_relationship,
    contact_1_phone,
    contact_2_name,
    contact_2_relationship,
    contact_2_phone,
    linked_account_names,
    linked_account_balances,
):
    if not n_clicks:
        raise PreventUpdate
    income_history = {
        id_["year"]: (val if val is not None else 0)
        for id_, val in zip(income_ids, income_values)
    }
    linked_accounts = [
        {
            "name": (name or "").strip() or "New account",
            "balance": balance if balance is not None else 0,
        }
        for name, balance in zip(linked_account_names, linked_account_balances)
    ]
    profile = {
        "age": age if age is not None else PROFILE_DEFAULTS["age"],
        "city": (city or "").strip() or PROFILE_DEFAULTS["city"],
        "state": (state or "").strip() or PROFILE_DEFAULTS["state"],
        "filing_status": filing_status or PROFILE_DEFAULTS["filing_status"],
        "children_count": children_count if children_count is not None else 0,
        "savings_balance": savings_balance if savings_balance is not None else 0,
        "savings_provider": PROFILE_DEFAULTS["savings_provider"],
        "retirement_401k_balance": k401_balance if k401_balance is not None else 0,
        "retirement_401k_provider": PROFILE_DEFAULTS["retirement_401k_provider"],
        "retirement_goal_age": goal_age if goal_age is not None else PROFILE_DEFAULTS["retirement_goal_age"],
        "annual_income": annual_income if annual_income is not None else 0,
        "income_history": income_history,
        "contact_1_name": (contact_1_name or "").strip() or PROFILE_DEFAULTS["contact_1_name"],
        "contact_1_relationship": (contact_1_relationship or "").strip() or PROFILE_DEFAULTS["contact_1_relationship"],
        "contact_1_phone": (contact_1_phone or "").strip() or PROFILE_DEFAULTS["contact_1_phone"],
        "contact_2_name": (contact_2_name or "").strip() or PROFILE_DEFAULTS["contact_2_name"],
        "contact_2_relationship": (contact_2_relationship or "").strip() or PROFILE_DEFAULTS["contact_2_relationship"],
        "contact_2_phone": (contact_2_phone or "").strip() or PROFILE_DEFAULTS["contact_2_phone"],
        "linked_accounts": linked_accounts,
    }
    years, current_total, shortfall, savings_target = compute_shortfall_estimate(profile)
    estimate_note = (
        f"Demo estimate only: the savings target uses a traditional retirement-calculator "
        f"rule (projects your current income to your goal age at 3%/year raises, assumes you'll "
        f"need 80% of that in retirement, then applies the standard 4%-withdrawal-rule 25x "
        f"multiplier) and updates instantly as you change age, retirement goal age, or income. "
        f"The amount-short estimate below assumes the current ${current_total:,.0f} grows by 5% "
        f"annually for {years} years with no additional contributions, and updates when you "
        "press Save. Illustrative only, not financial advice or a personalized projection."
    )
    return (
        profile,
        "Saved.",
        f"${shortfall:,.0f}",
        f"${savings_target:,.0f}",
        estimate_note,
        build_income_figure(income_history),
    )


if __name__ == "__main__":
    app.run(debug=False, port=8050)
