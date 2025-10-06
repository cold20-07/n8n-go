#!/usr/bin/env python3
"""
Interactive Prompt Assistant for N8N Go
Breaks down complex requests and guides users with yes/no questions
"""

import json
import re
from typing import Dict, List, Any, Optional

class InteractivePromptAssistant:
    def __init__(self):
        self.conversation_state = {
            'current_step': 0,
        )_assistant(eractive  demo_intn__":
  __mai__ == "me)

if __na + "="*50\n"("nt        pri
response)      print(quest)
  _request(remplexndle_cot.hastan= assi   response 
      * 30)"-"     print(  
 t}'"): '{requesest Case {i}\n📝 Tprint(f"     
   s, 1):requestate(test_umerin eni, request 
    for    " * 50)
 rint("=mo")
    pistant Deompt Assteractive Prrint("🤖 In    
    p
    ]
tions"nd notificaa aith dathing womet     "Sts",
   Google Sheelack to "Connect S     s",
   reportily y damate muto    "A
    a email",ts vi send resuliles andSV fprocess Ct to  wan       "Iuests = [
 st_reqs
    tecase
    # Test )
    Assistant(pteractivePromInt = istant"
    assant""ive assistracte intetrate th"""Demonst():
    e_assistanteractivmo_indef ded testing
ge anxample usa"

# Et you need?larify whald you cCou with that. elpo how t hsurem not eturn "I'       r 
   '])
     t_steptate['currensation_sverlf.con se(plan,on_questionslarificatiself.ask_c   return            += 1
   tep']nt_sate['curreversation_st self.con            
   ionstto next que  # Move          
               
      onseresper_on] = usses'][questioner_resp['uson_statetif.conversa  sel         ]
     ep][current_stclarify'estions_to_quplan['estion =    qu           
  ]):rify'la_to_cuestionslen(plan['qep < urrent_st     if c
       the response    # Store 
             n']
       kflow_plaworte['starsation_lf.conve = se   plan       tep']
  'current_stion_state[versap = self.conteent_srr      cu  ons
    uestiation qarificnses to cle respo Handl      #:
      ns"ion_questioatic "clarifxt ==tent_conif curre el
               sage']
esalysis['mesponse_ann r  retur            
       else:     "
  plan?he ut tnge aboto chaike d lly what you'ficale speci you tell mnd. Couldundersta return "I             
   'no': == e']nse_typysis['respoesponse_anal   elif r)
         lan, 0ons(p_questirificationlaelf.ask_cturn s re          ']
     anow_pl'workflation_state[converself.   plan = s        ions
     estled qu detaiStart asking    #          'yes':
   e_type'] == sis['respons_analy response   if               
    val")
  ro, "plan_appsponse_rense(userresporocess_user_ = self.panalysis  response_          roval":
= "plan_appext =ntrent_co      if cur
  "t""ent contexurrbased on crsation onvee the ctinu"Con""     > str:
   tr) -ntext: surrent_co, cse: strser_respon(self, utionnue_conversaf conti  de   
  
"""
  or D**C, A, B, typelease 

**P mindin have at you know whLet me- ** semething elD) Sotems
**between sysnc data or syations licappferent onnect dif** - Cration Integ) System 
**Csses ocebusiness prsks or titive taate repeon** - Automtiness AutomaBusi*B) abases
*s/datrom file ftasform daan tr, ornalyzess, a Proceng** -ata Processi) Dgoal:

**Acribes your  desf these besthich ou tell me wcould yoyou need, stand what underter "

To betnput}ser_i{u "oned:tiyou men see *

Iworkflow!*ct e perfeu create thp yont to hel wa*I
🤔 *""f"  return "
      ow type""orkflne the wn't determi cawhen wefication c clari"Ask basi   ""r:
     tr) -> stser_input: slf, uation(se_clarificfor_basicsk_ 
    def a_input)
   er(usation_clarificasicsk_for_bn self.a    retur     n
   ificatiofor clarttern, ask he pa determine twe can't# If            else:
   an)
      _user(pltoesent_plan_urn self.pr     ret      ser
 an to u Present pl 3:  # Step
                       plan
w_plan'] =rkflowoion_state['ersat self.conv           ser_input)
n'], uested_patteruggalysis['splan(anworkflow_.create_ = self     plan       3:
e'] > 0.['confidencysisf anal       i plan
  Create a # Step 2:            
  nput)
 t(user_iues_reqlyze_userlf.anasis = sealy      anest
   the requlyzep 1: Ana      # Ste"
  quests""er reusex dle complo han tmethodMain """
        tr) -> str:r_input: s useself,x_request(ndle_comple  def ha 
  
    summaryeturn    r   
    "
     
""RT')e 'RESTA(typroach rent appwith a diffeer t ov)
3. StarODIFY''M plan (type ges to thee chan. MakERATE')
2ype 'GENow (te workflow nenerate the to:
1. G mu likeld yo*

Woulow!*r WorkfGenerate Youady to 🚀 **Re""
mary += "       sum        
 \n"
answer}on}\n   → {{questi"{i}.  fry +=  summa       
   ), 1):s.items(seresponumerate(wer) in ennsion, aest(qu   for i,            
 *
"""
 nces:*Prefere

**Your ium')}ty', 'Med('complexin.get {plaplexity:**ow')}
**Comorkfl 'Custom Ww_name',kfloget('worpe:** {plan.ow Ty

**Workfl**e! Completrationigurkflow Conf**Wo""
✅ ary = f" summ             
{})
  , _plan't('workflowon_state.gersatinve= self.co   plan      })
es', {r_responsget('usetate.sation_self.converes = s  respons"
      rmation""cted infollewith all co summary kflowfinal wor""Generate   "str:
      elf) -> ummary(s_workflow_ste_finalef genera    
    dsult
rn re     retu    
     'NO'?"
  YES' or th 'espond wiu please ro. Could yos or nyeat's a  if thnot sure = "I'm message']lt['esu        rrify'
    'clation'] = next_ac[' result           
lear''] = 'uncnse_typelt['resposu   re        e:
  els           
      d?"
  instea need e what youou tell m Could yt.righte  isn't quiand this "I underste'] =ssagme   result['e
         tion'] = Truicaneeds_clarifsult['   re  fy'
       'clari] = ction'['next_a   result        '
 '] = 'nopese_tyespon['r  result        ):
  ferent']dif 'wrong', ''no', 'n', [ for word inleanse_c user_respon(word in  elif any     
              ion:"
   uestt q the next! Moving to"Perfecmessage'] = lt['   resu        on'
     esti_qu 'nextn'] =['next_actio  result          else:
                
"workflow: your  customizetions toquesk a few as! Let me eate'] = "Grlt['messag   resu      ls'
       tai 'ask_de =tion']lt['next_acesu        r        al":
plan_approvext == "nt       if co     = 'yes'
 _type']esponset['r   resul         ood']):
'right', 'gect', y', 'corr ' in ['yes', for wordsponse_cleaner_re usord inny(w   if anses
     no respok for yes/ # Chec
           }
     
       ': Falseonificatis_clar     'need     
  ': '', 'message
           rify',cla: 'on'next_acti '      wn',
      'unkno':e_typerespons     '
       esult = {     r 
        .lower()
  nse.strip()po = user_ressponse_cleanre     user_"""
   tion ace nextinrmnd dete response ayes/nos user's """Proces
        tr, Any]:-> Dict[sal") n_approv"plastr = ext:  str, contonse:f, user_respsponse(seler_reprocess_us def 
    
   rn response  retu  
         ""
   d)
"need insteame what you ase tell , pleNO**
(If NO or nswer YESase aPle**on}



{questi'])}:**rifytions_to_cla'quesen(plan[f {l1} ondex + question_iQuestion {"""
❓ ** fponse =
        res        on_index]
y'][questis_to_clarifstionan['queplstion =        que   
    
  _summary()loworkfrate_final_wgenern self.tu         re:
   _clarify'])ons_toestiplan['qudex >= len(stion_inif que        """
e by one onon questionstificalari """Ask c    :
   ) -> strnt = 0ion_index: iAny], questict[str,  plan: Dions(self,on_questrificatif ask_cla
    desponse
    turn re      re      
  
"""
  renting diffeethomed s' if you neNOype '
- Tcorrects oks lohie 'YES' if t Typeve?**
-ant to achit you w match whalan*Does this p']}

❓ *esstimated_nodplan['eodes:** {timated NEs
**exity']}plan['complty:** {Complexitimated **Esf"""
esponse +=       r
         }\n"
 {step. f"{i}response +=          
   s'], 1):n['stepplaumerate(in en step     for i,
    
        
"""nclude:**s I'll i]}

**Steption'escripn['dla** {pDescription:

**flow:**r your workplan fo*Here's my }**

📋 *low_name']orkf: {plan['wcreate want to erstand you*I und""
🎯 *"e = f     respons"
   t"" formar-friendly use in akflow planent the wor"Pres  ""
      r: -> sty])str, An plan: Dict[self,ser(t_plan_to_u def presen 
      urn plan
 ret 
          ] -= 1
    mated_nodes'['esti    plan       'Simple'
 plexity'] = ['coman          pl)) < 10:
  t.split(npuen(user_ielif l3
        es'] += timated_nodplan['es           igh'
 ty'] = 'Homplexi   plan['c       
  ):put.lower( user_inlex' inor 'comp 20 )) >nput.split( len(user_i   if
     ywordsength and kenput lased on ixity bleompAdjust c#     
      }
              
s'].copy()estionn['qu': patterlarifyto_ctions_  'ques
          dium','Mey': itcomplex         'd
   gger and en for tri + 2,  # +2['steps'])en(patternes': ld_nodteima       'esty(),
     '].copttern['stepseps': pa        'st}'",
    putr_inest: '{useequn your red o f"Basescription':          'd
  me'],natern['ame': pat'workflow_n            = {
       plan     
  n_type]
   ns[patterkflow_patterlf.worttern = se     pa  ""
 tern"on the patn based rkflow pladetailed wo"Create a "" 
       r, Any]:ict[st> Dt: str) -r, user_inpu_type: strntte(self, paanworkflow_pl create_  
    def }
  s
       ern_scorepattl_scores': 'al           ce,
 onfidennfidence': c      'co    tern,
  ': best_pated_patternuggest    's    
    {   return 
         )
    t_pattern]eywords[bes len(k_pattern] /cores[bestn_s= patterdence      confi)
   es.get_scor=patterneyores, kscax(pattern_ern = m  best_patt     ttern
 atching pa best mhe # Get t
       
        coretern] = sres[patcon_ster   pat       r)
  _input_loweern uskeyword is if ern_keyword patt in keywordum(1 for  score = s   
       s():temds.iin keywords tern_keyworattern, pat       for pores = {}
  pattern_sc        pattern
re each Sco      #  
  }
              ]
o'', 'trometween', 'fte', 'btegrahook', 'inweb', '', 'api'syncconnect', ation': [' 'integr         
  '], 'slack 'email',ify',, 'if', 'notn'er', 'whe 'trigghedule',', 'scatetomation': ['auutom          'aile'],
   'fl', 'data',', 'exce'csver', lt, 'fiorm'ze', 'transfanalyocess', '['pressing': _proc 'data        rds = {
   ywo      keerns
  nt pattreiffer deywords fo        # K
       lower()
 put. user_input_lower =ser_in   u"
     tern""orkflow pat best wmine theeterut and dyze user inp"""Anal  
      t[str, Any]:Dicstr) -> put:  user_int(self,uesuser_reqe_ef analyz  
    d   }
             }
         ]
        lly?'
      manuaormatically uto happen at this toyou wan      'Do              n?',
 ed conversio neformats thatent data fer use difsystemshe        'Do t            ,
 ?' regularlyeen systemsetwata bo sync do you need t'D                   
 vices?', or serapplicationsrent ct two diffeonnent to c you wa      'Do       : [
       s' 'question         
               ],      tem'
 ystion s to destina    'Send         ',
       a formatansform dat     'Tr          
      source', data from 'Get                 tem',
  ys first st tonnecCo     '              ': [
  'steps             ,
  tegration' 'System In'name':        {
        egration':         'int   },
                 ]
        
    letes?'compn this ne whemeootify soneed to nou    'Do y              
   ate files?',ges, or cre send messa records, updatewant to  'Do you                 tion?',
  e taking acns befortioertain condik chec to c you need     'Do          ?',
     appensc h specifi somethingle or when on a schedurunthis to  you want  'Do               [
    estions':   'qu         
             ],        ons'
 notificati    'Send             tions',
   e acExecut      '              ,
s'ons/rule conditi'Check                 rs',
   event occugger      'Tri             [
  eps':   'st          on',
    matirocess Autoss Pine'Bus'name':          {
       utomation':          'a },
        
         ]          
   il?'ia emand vsese, or  databae,o a filhe results to save tyou want to  'D                
   ?', datae this, or analyznsformer, traeed to filt   'Do you n         
        ases?',s, or databfiles, APIrom s data froceso pt t 'Do you wan                   ions': [
    'quest      ,
             ]'
         ion destinatlts to  'Save resu               
    data',process the ansform/   'Tr                  source',
 data from 'Get                
   steps': [         '     ow',
  flcessing Workro: 'Data P 'name'               g': {
rocessindata_p          's = {
  ernorkflow_patt self.w   kdown
    ir brea and theatternsworkflow p# Common          
  }
       
      ]_needed': [onsicatilarif'c      {},
      lan': kflow_por       'w
     },onses': {_resp    'user