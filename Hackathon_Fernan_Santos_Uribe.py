import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt


st.title("HACKATHON 2020 DATA WAREHOUSE")

st.write("""## **Integrantes**""")
st.write("""### Juan David Fernández, Laura Santos y Julián Uribe""")
st.write("""### Herramienta interactiva para explorar data de producción fiscalizada de crudo de la ANH""")


st.write("""## **Importar archivo**""")

ruta = st.text_input('Ingrese la ruta del archivo:')


if ruta:
    @st.cache
    def load_data():

        df = pd.read_excel(ruta)
        decimals = pd.Series(0, index=[df.columns[5:]])
        df = df.round(decimals)
        return df

    st.write('## **Base de datos Dinámica**')
    df = load_data()

    #def dyn_table()

    def ranking_year(data):

        if Ano != 'Todos':

            data_n = data[data.Año == Ano].iloc[:,5:17].sum()

            st.write('## **Producción Mensual del año: **',Ano)

            x = data_n.index
            y = data_n.values

            fig = plt.figure()
            plt.bar(x, y)
            plt.xticks(rotation=60)
            plt.ylabel('Produccion [STBD]')

        else:

            data_n = data.groupby('Año').sum().sum(axis=1)

            if data_n.shape[0]>1:
                low = data.Año.min()
                high = data.Año.max()

                st.write('## **Producción Histórica Anual**')

                s = st.sidebar.slider('Seleccione rango de años', low, high, (low, high))
                x = data_n.index[s[0] - low:s[1] - low + 1]
                y = data_n.values[s[0] - low:s[1] - low + 1]
                fig = plt.figure()
                plt.bar(x, y)
                plt.xticks(np.arange(s[0], s[1] + 1, step=1))
                plt.ylabel('Produccion [STBD]')
            else:
                st.write('## Producción Anual')
                x = data_n.index
                y = data_n.values
                fig = plt.figure()
                plt.bar(x, y)
                plt.xticks(data_n.index)
                plt.ylabel('Produccion [STBD]')

        return st.pyplot(fig)


    def fig_ranking_h(data,name):

        if Ano == 'Todos':
            dep = data.iloc[:, :-1].groupby(name).sum().sum(axis=1).sort_values(ascending=False)

        else:
            dep = data[data.Año==Ano].iloc[:, :-1].groupby(name).sum().sum(axis=1).sort_values(ascending=False)

        st.write('## **Ranking de producción por : **', name)

        if dep.shape[0] == 1:

            st.write('## **Producción Fiscalizada de Crudo**')
            x = dep.index
            y = dep.values
            fig = plt.figure()
            plt.bar(x, y)
            plt.xticks(dep.index)
            plt.ylabel('Produccion [STBD]')

        elif dep.shape[0] < 6:
            lim_low = 1
            lim_high = dep.shape[0]
            name = 'Seleccione el número de ' + name + 's'
            n = st.sidebar.slider(name, lim_low, lim_high)
            x = dep.index[:n]
            y = dep.values[:n]
            fig = plt.figure()
            plt.barh(x, y)
            plt.gca().invert_yaxis()
            plt.xlabel('Produccion [STBD]')

        else:
            lim_low = 5
            lim_high = dep.shape[0]
            name = 'Seleccione el número de ' + name + 's'
            n = st.sidebar.slider(name, lim_low, lim_high)
            x = dep.index[:n]
            y = dep.values[:n]
            fig = plt.figure()
            plt.barh(x, y)
            plt.gca().invert_yaxis()
            plt.xlabel('Produccion [STBD]')

        return st.pyplot(fig)


    # Inician filtros
    a = np.sort(df['Año'].unique()).tolist()
    a.insert(0, 'Todos')
    Ano = st.sidebar.selectbox('Seleccione el Año', (a))

    if Ano == 'Todos':
        d = np.sort(df['Departamento'].unique()).tolist()
        d.insert(0, 'Todos')
        Departamento = st.sidebar.selectbox('Seleccione el Departamento', (d))

        if Departamento != 'Todos':

            df1 = df[df.Departamento == Departamento]

            o = np.sort(df1['Operadora'].unique()).tolist()
            o.insert(0, 'Todos')
            Operadora = st.sidebar.selectbox('Seleccione la Operadora', (o))

            if Operadora != 'Todos':

                df2 = df1[df1.Operadora == Operadora]


                c = np.sort(df2['Contrato'].unique()).tolist()
                c.insert(0, 'Todos')

                Contrato = st.sidebar.selectbox('Seleccione el Contrato', (c))

                if Contrato != 'Todos':

                    df3 = df2[df2.Contrato == Contrato]

                    m = np.sort(df3['Campo'].unique()).tolist()
                    m.insert(0, 'Todos')
                    Campo = st.sidebar.selectbox('Seleccione el Campo', (m))

                    if Campo != 'Todos':
                        df4 = df3[df3.Campo == Campo]
                        df4
                        ranking_year(df4)


                    else:
                        df3
                        ranking_year(df3)
                        fig_ranking_h(df3, 'Campo')

                else:
                    df2
                    ranking_year(df2)
                    fig_ranking_h(df2, 'Contrato')
                    fig_ranking_h(df2, 'Campo')

            else:
                df1
                ranking_year(df1)
                fig_ranking_h(df1, 'Operadora')
                fig_ranking_h(df1, 'Contrato')
                fig_ranking_h(df1, 'Campo')

        else:
            df
            ranking_year(df)
            fig_ranking_h(df, 'Departamento')
            fig_ranking_h(df, 'Operadora')
            fig_ranking_h(df, 'Contrato')
            fig_ranking_h(df, 'Campo')

    else:
        db = df[df.Año == Ano]

        d = np.sort(df['Departamento'].unique()).tolist()
        d.insert(0, 'Todos')
        Departamento = st.sidebar.selectbox('Seleccione el Departamento', (d))

        if Departamento != 'Todos':

            df1 = db[db.Departamento == Departamento]

            o = np.sort(df1['Operadora'].unique()).tolist()
            o.insert(0, 'Todos')
            Operadora = st.sidebar.selectbox('Seleccione la Operadora', (o))

            if Operadora != 'Todos':

                df2 = df1[df1.Operadora == Operadora]


                c = np.sort(df2['Contrato'].unique()).tolist()
                c.insert(0, 'Todos')

                Contrato = st.sidebar.selectbox('Seleccione el Contrato', (c))

                if Contrato != 'Todos':

                    df3 = df2[df2.Contrato == Contrato]

                    m = np.sort(df3['Campo'].unique()).tolist()
                    m.insert(0, 'Todos')
                    Campo = st.sidebar.selectbox('Seleccione el Campo', (m))

                    if Campo != 'Todos':
                        df4 = df3[df3.Campo == Campo]
                        df4
                        ranking_year(df4)


                    else:
                        df3
                        ranking_year(df3)
                        fig_ranking_h(df3, 'Campo')

                else:
                    df2
                    ranking_year(df2)
                    fig_ranking_h(df2, 'Contrato')
                    fig_ranking_h(df2, 'Campo')

            else:
                df1
                ranking_year(df1)
                fig_ranking_h(df1, 'Operadora')
                fig_ranking_h(df1, 'Contrato')
                fig_ranking_h(df1, 'Campo')

        else:
            db
            ranking_year(df)
            fig_ranking_h(df, 'Departamento')
            fig_ranking_h(df, 'Operadora')
            fig_ranking_h(df, 'Contrato')
            fig_ranking_h(df, 'Campo')