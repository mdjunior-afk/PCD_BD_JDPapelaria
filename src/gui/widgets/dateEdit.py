from PySide6.QtWidgets import *

class DateEdit(QDateEdit):
    def __init__(self, date):
        super().__init__(date=date)

        self.setDisplayFormat("dd/MM/yyyy")
        self.setCalendarPopup(True)

        self.setMinimumWidth(self.sizeHint().width() + 30)

        self.setStyleSheet(f"""
                           
        QCalendarWidget QAbstractItemView {{
            background-color: #F3F3F3; /* Fundo dos dias */
            selection-background-color: #0A54C3; /* Fundo do dia selecionado (cor de destaque) */
            selection-color: white; /* Cor do texto do dia selecionado */
        }}
                           
        /* 2. Estilo da Janela de Calendário (Popup) */
        QCalendarWidget {{
            background-color: #F3F3F3 !important;/* Fundo principal do calendário */
            alternate-background-color: #F3F3F3; /* Garante que o fundo seja uniforme */
            
            /* Cor das linhas do grid, se visíveis */
            /* Note: Depende do estilo do sistema, mas tentamos forçar cores claras */
            gridline-color: lightgray;
            border: 1px solid lightgray;
        }}

        /* 3. Estilo dos Headers (Mês e Ano) */
        QCalendarWidget QWidget#qt_calendar_navigationbar {{
            background-color: #0A54C3; /* Cor de destaque (#0A54C3) */
            border-bottom: 1px solid #0A54C3;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }}

        /* Cor do texto do Mês e Ano no Header */
        QCalendarWidget QAbstractItemView:enabled {{
            color: #333333; /* Cor padrão do texto (dias/datas) */
        }}

        /* Cor do texto dos dias da semana (ex: Dom, Seg) */
        QCalendarWidget QAbstractItemView {{
            selection-background-color: #DDEFFF; /* Fundo quando um item está selecionado, mas ainda não é a data atual */
            selection-color: #000000;
            outline: none;
            border: none;
        }}

        /* 4. Estilo dos Botões de Navegação (< e >) */
        QCalendarWidget QToolButton {{
            color: white; /* Cor do ícone do botão */
            background-color: #0A54C3; /* Fundo do botão, mesma cor da navigation bar */
            icon-size: 18px;
            margin: 5px;
            border-radius: 4px;
        }}

        QCalendarWidget QToolButton:hover {{
            background-color: #0044A3; /* Cor mais escura no hover */
        }}

        QCalendarWidget QToolButton:pressed {{
            background-color: #003388;
        }}

    /* 📌 1. ESTILO DO FUNDO DOS DIAS DA SEMANA */
        QCalendarWidget QWidget#qt_calendar_days_of_week {{
            background-color: lightgray !important; /* Fundo cinza claro, contraste com o #F3F3F3 */
            border-bottom: 1px solid lightgray; /* Adiciona uma linha divisória discreta */
        }}
        
        /* 📌 2. ESTILO DA FONTE DOS DIAS DA SEMANA */
        /* Este seletor afeta os nomes dos dias (Dom, Seg, etc.) */
        QCalendarWidget QAbstractItemView {{
            /* Garante que o texto seja escuro (preto/cinza escuro) */
            color: #333333; 
        }}
                           
        /* 6. Estilo dos Dias Individuais (Datas) */
        QCalendarWidget QAbstractItemView:enabled {{
            color: #333333; /* Cor padrão dos dias */
        }}

        /* Estilo para Dias do mês anterior/próximo (cinza claro) */
        QCalendarWidget QAbstractItemView:disabled {{
            color: #AAAAAA;
        }}

        /* Estilo para a Data Atual (Today) */
        QCalendarWidget QAbstractItemView:enabled:!selected {{
            /* Borda circular discreta para o dia de hoje */
            /* Nota: Qt é rígido em estilizar o Today */
        }}

        /* Estilo para o Dia Selecionado (a data que o usuário clicou) */
        QCalendarWidget QAbstractItemView:selected {{
            background-color: #0A54C3; /* Fundo do dia selecionado: Cor de destaque */
            color: white; /* Cor do texto branco */
            border-radius: 4px; /* Cantos arredondados */
        }}
        """)
