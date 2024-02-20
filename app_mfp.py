# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 10:05:17 2024

@author: Gebruiker
"""
#%%
import numpy as np
import math
import pandas as pd
import openpyxl
import base64
import io
#%%

import numpy as np
import math
import streamlit as st
import pandas as pd
import altair as alt
import base64
import io




st.set_page_config(page_title="Financiële Planning")

st.title("Financiële Planning")

st.markdown("Voer uw gegevens in om te berekenen hoeveel u maximaal kunt lenen en hoe groot uw eigenwoningsschuld zal zijn!")

tab1, tab2, tab3 = st.tabs(["Hypotheek","Eigenwoningsschuld","Aflossing"])



AOW_leeftijd = 68

with tab1:
    column1, column2, column3 = st.columns(3)
    VOOR_AOW = pd.read_excel(r"C:\Users\Gebruiker\OneDrive - Office 365 Fontys\Documenten\Privé\Programmeren\Financieringspercentages_Annuiteitenfactor.xlsx",sheet_name='Voor AOW')
    NA_AOW = pd.read_excel(r"C:\Users\Gebruiker\OneDrive - Office 365 Fontys\Documenten\Privé\Programmeren\Financieringspercentages_Annuiteitenfactor.xlsx",sheet_name='Na AOW')
    annuiteitentabel = pd.read_excel(r"C:\Users\Gebruiker\OneDrive - Office 365 Fontys\Documenten\Privé\Programmeren\Financieringspercentages_Annuiteitenfactor.xlsx",sheet_name='Annuiteitenfactor') 
    studieschuldtabel = pd.read_excel(r"C:\Users\Gebruiker\OneDrive - Office 365 Fontys\Documenten\Privé\Programmeren\Financieringspercentages_Annuiteitenfactor.xlsx",sheet_name='Studieschuld') 
    studieschuldtabel['Debetrente'] = studieschuldtabel['Debetrente'].apply(lambda x: f"{x:.3f}".replace('.',','))
    
    with column1:
        st.subheader("Partnerschap")
        
    # input vanuit gast
        gez_ink = st.number_input("_Gezamenlijk bruto jaarinkomen_", 0,999999999,0)
        toetsinkomen = 500 * math.floor(gez_ink/500)
        #st.write(f"Het gezamenlijk brutojaarinkomen is €{gez_ink}")
    # leeftijd nodig voor AOW-leeftijd: JA/NEE    
        leeftijd = st.number_input("_Leeftijd oudste partner_",0,120,18)
    #    st.write(f"De oudste partner is {leeftijd} jaar.")
        waarde_woning = st.number_input("_Marktwaarde woning_",0,99999999,250000)

        st.write("---------------------------")

    
    with column2:
        st.subheader("Financiering")
    # Rente nodig die ze willen. Als tijd <= 10 jaar: 5%
        rentepercentage = st.number_input("_Rentepercentage zonder procentteken_",step=0.01,value=5.00)
        #st.write(f"De rente vastzetten op een hoogte van {rentepercentage:.3f}%")
    # tijdsperiode naar wensen. 
        tijdsperiode = st.selectbox("_Looptijd in maanden_",['120','180','240','300','360'])
        #st.write(f"De looptijd voor de hypotheek is {tijdsperiode} maanden.")
    # Als tijd < 10 dan toetsrente van 5%    
        if tijdsperiode == '120':
            debetrente = 5
            debetrente = "{:,.3f}".format(debetrente)
            debetrente = debetrente.replace('.', ',')
        #    st.write(f"De debetrente is {debetrente}%")
    # Als de tijd groter is dan 10 jaar, dan de werkelijke rente    
        else:
            if rentepercentage < 1.50:
                debetrente = "1,500"
            elif rentepercentage > 6.501:
                debetrente = "6,501"
            else:
                debetrente = math.floor(rentepercentage+0.5)
                debetrente = "{:,.3f}".format(debetrente)
                debetrente = debetrente.replace('.', ',')
                
           # st.write(f"De debetrente is {debetrente}%")

    # leeftijd controleren voor juiste financieringslastpercentage.
        if leeftijd < AOW_leeftijd:
            woonquote = VOOR_AOW.loc[VOOR_AOW['toetsinkomen'] == toetsinkomen, debetrente].values[0]
            #st.write(f"Het financieringslastpercentage is {woonquote}")
        else:
            woonquote = NA_AOW.loc[NA_AOW['toetsinkomen'] == toetsinkomen, debetrente].values[0]
            #st.write(f"Het financieringslastpercentage is {woonquote}")
            
        finan_ink = gez_ink * woonquote
        #st.write(f"Hiermee komt het financieringslastinkomen op €{finan_ink:.2f}")
        
        finan_ink_maand = finan_ink/12
        #st.write(f"Maandelijks komt dit uit op €{finan_ink_maand:.2f}")
        
        
    with column3:
        st.subheader("Schulden")
        
        #lasten
        schuld_1 = st.number_input('_Oplopende schuld 1 (bijv.rekening courant)_',value=0)
        schuld_2 = st.number_input('_Oplopende schuld 2 (bijv. kredietlimiet)_',value=0)
        schuld_3 = st.number_input('_Aflopende schuld (bijv. aflopend krediet)_',value=0)
        schuld_4 = st.number_input(label='_Maandelijkse last studieschuld_',value=0)
    # juiste factor/opslag op maandelijkse lasten studieschuld mbt tot debetrente    
        if schuld_4 is not None:
            factor_studieschuld = studieschuldtabel.loc[studieschuldtabel['Debetrente'] == debetrente,'Opslag'].values[0]
            mnd_studieschuld = factor_studieschuld*schuld_4
        else:
            mnd_studieschuld = 0
        tot_mnd_schuld = schuld_1*0.02 + schuld_2*0.02 + schuld_3 + mnd_studieschuld
        
        st.markdown(
            """
            <style>
                .container-style {
                    padding: 10px;
                    border: 2px solid black;
                    border-radius: 5px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Inhoud van de container
        st.write(f'<div class="container-style">De totale maandelijkse schuld is €{tot_mnd_schuld}</div>', unsafe_allow_html=True)
    
        st.write("---------------------------")
    # annuïteitenfactor   
        ann_bedrag = finan_ink_maand - tot_mnd_schuld
        ann_rente = round(rentepercentage/100,3)
        
        ann_factor = annuiteitentabel.loc[annuiteitentabel['Rentepercentage'] == ann_rente, f'{tijdsperiode}'].values[0]
        hypo_LTI = ann_factor*ann_bedrag
        
    # uiteindelijke button om te zien hoeveel er maximaal geleend kan worden.    
    with column1:
        st.subheader("_Resultaat_")
        if st.checkbox("Max hypotheek (LTV)"):
            st.write(f"U kunt maximaal €{waarde_woning} lenen.")
        if st.checkbox("Max hypotheek (LTI)"):
            st.write(f'U kunt maximaal €{hypo_LTI:.0f} lenen.')    
        st.write("---------------------------")
        if st.button("Conclusie"):
            if hypo_LTI < waarde_woning and hypo_LTI > 0:
                st.write(f"U kunt maximaal €{hypo_LTI:.0f} lenen.")
            else:
                st.write(f"U kunt maximaal 100% van de waarde\n van de woning lenen, t.w.v. €{waarde_woning}")


with tab2:
    #st.subheader("EWR")
    column_1, column_2, column_3 = st.columns(3)
    with column_1:
        st.subheader("EWR")
        verkoop_woning = st.number_input("_Verkoopwaarde woning_",0,99999999,300000)
        verkoop_makelaar = st.number_input("_Verkoopmakelaar_",0,9999999,5000)
        oude_EWS = st.number_input("_Oude openstaande EWS_",value=50000)
        partner_EWR = st.selectbox('Tot wie behoort het eigenwoningreserve (EWR)?',('Partner 1','Partner 2','Beiden'))
        

        if verkoop_woning and verkoop_makelaar and oude_EWS is not None:
            EWR = verkoop_woning - verkoop_makelaar - oude_EWS
            #st.write(f"De eigenwoningreserve heeft een waarde van €{EWR:.0f} en hoort bij {partner_EWR}")               
            st.write("-----------------")
            uitzondering_1 = st.checkbox(f"Is er door {partner_EWR} langer dan 3 jaar gehuurd?")
            uitzondering_2 = st.checkbox(f"Is de woning van {partner_EWR} nog niet verkocht?")
            if uitzondering_1:
                st.write("_Ja_")
            if uitzondering_2:
                st.write("_Ja_")
            st.divider()
            if uitzondering_1 or uitzondering_2:
                EWR = 0
                st.write(f"De EWR kent een waarde van €{EWR:.0f} en behoort tot {partner_EWR}.")
            else:
                EWR = EWR
                st.write(f"De EWR kent een waarden van €{EWR:,.0f}".replace('.',',').replace(',', '.',1), f"en behoort tot {partner_EWR}")
                
    with column_2:
        st.subheader("Kosten")
        st.caption('Verwervingskosten')
    # verwervingskosten    
        aankoop_woning = st.number_input("_Aankoop woning_",0,99999999,waarde_woning)
        overdrachtsbelasting = 0.02*aankoop_woning
        transportakte = st.number_input("_Transportakte_",0,99999999,0)
        verbouwing = st.number_input("_Verbouwing_",0,99999999,0)
    # financieringskosten    
        st.caption('Financieringskosten')
        aankoop_makelaar = st.number_input("_Aankoopmakelaar_",0,99999999,0)
        hypotheekakte = st.number_input("_Hypotheekakte_",0,99999999,0)
        taxatie = st.number_input("_Taxatierapport_",0,99999999,0)
        advieskosten = st.number_input("_Advieskosten_",0,99999999,0)
        finan_kosten = st.number_input("_Financieringskosten_",0,99999999,0)
        
        financieringskosten = aankoop_makelaar + hypotheekakte + taxatie + advieskosten + finan_kosten
        #st.write(f"De totale financieringskosten zijn €{financieringskosten:.0f}")
        
        # uitzonderingen waardoor: EWR = 0
        # EWR = verkoop - verkoopmakelaar - oude EWS
        # EWR hoort bij partner 1 of 2 ? of allebei een andere ewr?
        # verdeling partner schap 50/50
    with column_3:
        st.subheader('EWS')
        EWS = aankoop_woning + overdrachtsbelasting + transportakte + verbouwing 

        if partner_EWR == 'Beiden':
            EWS = aankoop_woning + overdrachtsbelasting + transportakte + verbouwing - EWR
            st.write(f"De EWS is voor jullie samen €{EWS:,.0f}".replace('.',',').replace(',', '.',1))
            max_ews = EWS + financieringskosten
        # als de max ews kleiner is dan het te lenen bedrag, dan naar rato verdelen:
            if max_ews < min(hypo_LTI, waarde_woning): 
                financieringskosten_2 = (EWS/min(hypo_LTI, waarde_woning)) * financieringskosten
                max_ews = EWS + financieringskosten_2
                box_3 = min(hypo_LTI, waarde_woning) - max_ews
                st.write(f"Max EWS in box 1 is €{max_ews:.0f}.")
                st.write(f"Max EWS in box 3 is €{box_3:.0f}.")
            else: 
               max_ews = EWS + financieringskosten
               st.write(f"Max EWS is €{max_ews:,.0f}".replace('.',',').replace(',', '.',1))
        else:
            EWS_ewr = EWS/2 - EWR
            andere_partner = EWS_ewr + EWR

            if ( EWS_ewr + financieringskosten/2 ) < (min(hypo_LTI, waarde_woning)/2):
                financieringskosten_3 = (EWS_ewr/(min(hypo_LTI, waarde_woning)/2)) * financieringskosten/2
                max_ews_partner_box1 = EWS_ewr + financieringskosten_3
                max_ews_partner_box3 = ( min(hypo_LTI, waarde_woning)/2 ) - max_ews_partner_box1
             #   st.write(f"De maximale EWS in box 1 voor {partner_EWR} is €{max_ews_partner_box1:.2f} ")
             #   st.write(f"De maximale EWS in box 3 voor {partner_EWR} is €{max_ews_partner_box3:.2f} ")

                data = pd.DataFrame({
                        'Box': ['Box 1', 'Box 3'],
                        'Max EWS': [f"€{max_ews_partner_box1:,.2f}".replace('.',',').replace(',', '.',1), f"€{max_ews_partner_box3:,.2f}".replace('.',',').replace(',', '.',1)]})
                st.write(f"_Maximale eigenwoningsschuld voor {partner_EWR}_:")
                st.table(data)
            else:
                max_ews_partner_box1 = EWS_ewr + financieringskosten/2
                st.write(f"De maximale EWS is geheel in box 1 en kent een waarde van €{max_ews_partner_box1:,.0f}".replace('.',',').replace(',', '.',1))
        #    st.write("---------------------")
            max_ews_partner = andere_partner + (financieringskosten/2)
            if uitzondering_1 or uitzondering_2:
                st.write(" ")
            else:
                st.write(f"De maximale EWS voor de partner zonder EWR is €{max_ews_partner:,.0f}".replace('.',',').replace(',', '.',1), "geheel in box 1.")
            st.write('----------------')
     
        
with tab3:
   # kolom1, kolom2 = st.columns(2)
   # with kolom1:
    def lineaire_hypotheek(hoofdsom, looptijd_maanden, rentepercentage):
        
        looptijd_maanden = int(tijdsperiode)
        maandelijkse_rente = rentepercentage/100/12
        maandelijkse_aflossing = hoofdsom/looptijd_maanden
        resterende_schuld = hoofdsom
            
        aflossingen = []
        rentebedragen = []
        resterende_schulden = []
        bruto_maandlasten = []
            
        for maand in range(1,looptijd_maanden+1):
            rente = resterende_schuld * maandelijkse_rente
            aflossing = maandelijkse_aflossing
            resterende_schuld -= aflossing
            bruto_maandlast = aflossing + rente
                
            aflossingen.append(aflossing)
            rentebedragen.append(rente)
            resterende_schulden.append(resterende_schuld)
            bruto_maandlasten.append(bruto_maandlast)
            
        df = pd.DataFrame({
                'Maand': list(range(1, looptijd_maanden + 1)),
                'Aflossing': [round(getal, 2) for getal in aflossingen],
                'Rente': rentebedragen,
                'Resterend': [round(getal,2) for getal in resterende_schulden] ,
                'Bruto maandlast': [round(getal,2) for getal in bruto_maandlasten] 
            })
        
        data_grafiek = pd.DataFrame({
                'Maand': list(range(1, looptijd_maanden + 1)),
                'Aflossing': [round(getal, 2) for getal in aflossingen],
                'Rente': rentebedragen,
                'Resterend': [round(getal,2) for getal in resterende_schulden] ,
                'Bruto maandlast': [round(getal,2) for getal in bruto_maandlasten] 
            })
        

        df['Aflossing'] = df['Aflossing'].apply(lambda x: f"€{x:,.2f}".replace('.', ',').replace(',', '.', 1))
        df['Rente'] = df['Rente'].apply(lambda x: f"€{x:,.2f}".replace('.', ',').replace(',', '.', 1))
        df['Resterend'] = df['Resterend'].apply(lambda x: f"€{x:,.2f}".replace('.', ',').replace(',', '.', 1))
        df['Bruto maandlast'] = df['Bruto maandlast'].apply(lambda x: f"€{x:,.2f}".replace('.', ',').replace(',', '.', 1))
        

        
        # tabel met samenvattende gegevens zoals sommaties.
        
        tot_rente = sum(rentebedragen)
        tot_bruto_mndlasten = sum(bruto_maandlasten)
        
        data = pd.DataFrame({
                    'Soort last': ['Hypotheek','Maandelijkse aflossing', 'Totale rente', 'Totale bruto last'],
                    'Bedrag': [hoofdsom, aflossing, tot_rente,tot_bruto_mndlasten]})
        data['Bedrag'] = data['Bedrag'].apply(lambda x: f"€{x:,.2f}".replace('.',',').replace(',', '.',1))
        st.dataframe(data.set_index(data.columns[0]))
        st.caption('**Bovenstaande tabel geeft de uiteindelijke totale kosten weer van de lineaire aflossing.**')
   #     st.write('---------')
        st.divider()
        
        
        # grafiek in de functie
        chart1 = alt.Chart(data_grafiek).mark_area(opacity=0.2, interpolate='linear', color='#ADC9F5').encode(
                x='Maand',y='Bruto maandlast')
        
        # Voeg een tweede lijn toe voor de aflossing
        line1 = alt.Chart(data_grafiek).mark_area(opacity=0.2,interpolate='linear',color='#FFAFB0').encode(
                x='Maand',y='Aflossing')
        
        chart2 = alt.Chart(data_grafiek).mark_line(color='#025AFF').encode(
                x='Maand',y=alt.Y('Bruto maandlast')).properties(width=600,height=400)
                
        line2 = alt.Chart(data_grafiek).mark_line(color='#FD181F').encode(
                x='Maand',y='Aflossing')       
        # Legenda maken
        legenda = alt.Chart(pd.DataFrame({'label': ['Rente', 'Aflossing'], 'color': ['#025AFF', '#FD181F']})).mark_text().encode(
                        y=alt.Y('label:N', axis=None),
                        color=alt.Color('color', scale=None),
                        text='label'
                    )
        # Combineer de grafieken
        chart = (chart1 + line1 + chart2 + line2) | legenda

        
        # Weergeef de grafiek in Streamlit
        if st.toggle('Grafiek'):
            st.altair_chart(chart, use_container_width=True)
            
      # specifiek maandnummer en zijn gegevens  
        if st.toggle('Specifiek maandnummer'):  
            keuze_maand = st.slider('Voer een maandnummer in waarvan u de cumulatieve gegevens wilt weten.',0,int(tijdsperiode),1)
            tot_aflossing_mnd = data_grafiek['Aflossing'].iloc[:keuze_maand].sum()
            tot_rente_mnd = data_grafiek['Rente'].iloc[:keuze_maand].sum()
            tot_bruto_mndlasten_mnd = data_grafiek['Bruto maandlast'].iloc[:keuze_maand].sum()
            
            data_mnd = pd.DataFrame({
                        'Soort last': ['Hypotheek','Totale aflossing', 'Totale rente', 'Totale bruto maandlast'],
                        'Bedrag': [hoofdsom, tot_aflossing_mnd, tot_rente_mnd,tot_bruto_mndlasten_mnd]})
            data_mnd['Bedrag'] = data_mnd['Bedrag'].apply(lambda x: f"€{x:,.2f}".replace('.',',').replace(',', '.',1))
            st.dataframe(data_mnd.set_index(data_mnd.columns[0]))
            st.caption(f"**Bovenstaande tabel geeft de totale kosten aan tot en met maand {keuze_maand}.**")
            st.write('---------')
        
        
        if st.toggle('Hele tabel'):
            st.dataframe(df.set_index(df.columns[0]))
            
            # buffer to use for excel writer
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer,engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1',index=False)
        #        writer.save()
            buffer.seek(0)
            download2 = st.download_button(label='Download tabel',data=buffer,
                                               file_name='lineaire_hypotheek.xlsx', 
                                               mime='applicaiton/vnd.ms-excel')
            if download2:
                st.balloons()
                
         #   bestand = df.to_excel('output1.xlsx')
         #   st.download_button(label='Download tabel', data=bestand, file_name='output1.xlsx')
           # return aflossingen, rentebedragen, resterende_schulden, bruto_maandlasten
        
        
        return data_grafiek
    

    hoofdsom = min(hypo_LTI, waarde_woning)
    if st.checkbox('Lineaire hypotheek'):
        lineaire_hypotheek(hoofdsom, tijdsperiode, rentepercentage)
        #df_resultaat = lineaire_hypotheek(hoofdsom, tijdsperiode, rentepercentage)
        


#%% financieringspercentages
import pandas as pd
VOOR_AOW = pd.read_excel(r"C:\Users\Gebruiker\OneDrive - Office 365 Fontys\Documenten\Privé\Programmeren\Financieringspercentages_Annuiteitenfactor.xlsx",sheet_name='Voor AOW')
NA_AOW = pd.read_excel(r"C:\Users\Gebruiker\OneDrive - Office 365 Fontys\Documenten\Privé\Programmeren\Financieringspercentages_Annuiteitenfactor.xlsx",sheet_name='Na AOW')
studieschuldtabel = pd.read_excel(r"C:\Users\Gebruiker\OneDrive - Office 365 Fontys\Documenten\Privé\Programmeren\Financieringspercentages_Annuiteitenfactor.xlsx",sheet_name='Studieschuld') 
annuiteitentabel = pd.read_excel(r"C:\Users\Gebruiker\OneDrive - Office 365 Fontys\Documenten\Privé\Programmeren\Financieringspercentages_Annuiteitenfactor.xlsx",sheet_name='Annuiteitenfactor') 
studieschuldtabel['Debetrente'] = studieschuldtabel['Debetrente'].apply(lambda x: f"{x:.3f}".replace('.',','))
        
# max LTI & LTV allebei weergeven
# LTI verplaatsen
# Eindantwoord weergeven    

#%%


#aflossingen, rentebedragen, resterende_schulden = lineaire_hypotheek(hoofdsom, looptijd_jaren, rentepercentage)
#print_aflossingstabel(aflossingen, rentebedragen, resterende_schulden)
