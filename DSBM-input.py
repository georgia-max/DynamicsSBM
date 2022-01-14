"""Tone & Tsutsui 2010 Dynanmic SBM DEA"""from gurobipy import*DMU = ['A','B','C','D','E','F','G','H']E={}E_term1,E_term2,E_term3,E_term4, E_total = {},{},{},{},{}E_all={}L={}Lnk={}T={}SO={}SI={}SL={}W={}for o in DMU:    #TODO change the data to Tone, Tsutsui (2010) Dynamic SBM DEA paper"    Terms=4 #terms    #Term input    T1I=1    T2I = 1    T3I = 1    T4I = 1    #term output    T1O = 1    T2O = 1    T3O = 1    T4O = 1    #carry over link    L12= 1    L23= 1    L34= 1    L45=1    "This data is from Tone, Tsutsui (2010) Dynamic SBM DEA paper"    DMU, T1x,T1y= multidict({('A'):[10,50],("B"):[30,150], ("C"):[20,50],("D"):[30,100],("E"):[30,150],("F"):[10,100],                          ("G"):[30,100],("H"):[20,100]})    DMU, T2x, T2y = multidict({('A'):[11,50],("B"):[33,150], ("C"):[22,100],("D"):[33,120],                                 ("E"):[33,135],("F"):[11,90], ("G"):[33,180],("H"):[22,40]})    DMU, T3x, T3y = multidict({('A'):[12,50],("B"):[36,150], ("C"):[24,150],("D"):[36,150],                                 ("E"):[36,120],("F"):[12,40], ("G"):[36,95],("H"):[24,150]})    DMU, T4x, T4y = multidict({('A'): [13,50], ("B"): [39,150], ("C"): [26,180], ("D"): [39,180],                                    ("E"): [39,105], ("F"): [13,35], ("G"): [39,200], ("H"): [26,100]})    DMU, Z12, Z23, Z34, Z45 =  multidict({('A'):[10,10,10,10],("B"):[20,25,30,35], ("C"):[30,30,30,30],("D"):[15,20,25,30],                                 ("E"):[20,25,30,35],("F"):[10,10,10,10], ("G"):[20,30,40,50],("H"):[10,10,10,10]})    lamd ={}    model = Model("DySBMDEA- input oriented")    #Add decision variables    # lamda_j_t    for t in range(Terms):        for j in DMU:            lamd[t, j] = model.addVar(vtype=GRB.CONTINUOUS, name="λ_%s_%s:" % (t, j))    #output slack    for t in range(Terms):        if t==0:            for r in range(T1O):                SO[t, r] = model.addVar(vtype=GRB.CONTINUOUS, name="SO%s_%s:" % (t, r))        elif t ==1:            for r in range(T2O):                SO[t, r] = model.addVar(vtype=GRB.CONTINUOUS, name="SO%s_%s:" % (t, r))        elif t ==2:            for r in range(T3O):                SO[t, r] = model.addVar(vtype=GRB.CONTINUOUS, name="SO%s_%s:" % (t, r))        elif t ==3:            for r in range(T4O):                SO[t, r] = model.addVar(vtype=GRB.CONTINUOUS, name="SO%s_%s:" % (t, r))        else:            pass    print(SO)    #input slack    for t in range(Terms):        if t == 0:            for i in range(T1I):                SI[t, i] = model.addVar(vtype=GRB.CONTINUOUS, name="SI%s_%s:" % (t, i))        elif t == 1:            for i in range(T2I):                SI[t, i] = model.addVar(vtype=GRB.CONTINUOUS, name="SI%s_%s:" % (t, i))        elif t == 2:            for i in range(T3I):                SI[t, i] = model.addVar(vtype=GRB.CONTINUOUS, name="SI%s_%s:" % (t, i))        elif t == 3:            for i in range(T4I):                SI[t, i] = model.addVar(vtype=GRB.CONTINUOUS, name="SI%s_%s:" % (t, i))        else:            pass    print(SI)    # free link slack    for t in range(Terms):        if t == 0:            for i in range(L12):                SL[t, i] = model.addVar(vtype=GRB.CONTINUOUS, name="SL%s_%s:" % (t, i))        elif t == 1:            for i in range(L23):                SL[t, i] = model.addVar(vtype=GRB.CONTINUOUS, name="SL%s_%s:" % (t, i))        elif t == 2:            for i in range(L34):                SL[t, i] = model.addVar(vtype=GRB.CONTINUOUS, name="SL%s_%s:" % (t, i))        elif t == 3:            for i in range(L45):                SL[t, i] = model.addVar(vtype=GRB.CONTINUOUS, name="SL%s_%s:" % (t, i))        else:            pass    print(SL)    model.update()    model.setObjective(        1/4*((1-SI[0,0]/T1x[o])+(1-SI[1,0]/T2x[o])+(1-SI[2,0]/T3x[o])+(1-SI[3,0]/T4x[o]))             , GRB.MINIMIZE)    #input contriant Eq#(2)    model.addConstr(quicksum(lamd[0,j] * T1x[j] for j in DMU) + SI[0,0] ==  T1x[o])    model.addConstr(quicksum(lamd[1,j] * T2x[j] for j in DMU) + SI[1,0] == T2x[o])    model.addConstr(quicksum(lamd[2,j] * T3x[j] for j in DMU) + SI[2,0] == T3x[o])    model.addConstr(quicksum(lamd[3, j] * T4x[j] for j in DMU) + SI[3, 0] == T4x[o])    # output contriant Eq#(2)    model.addConstr(quicksum(lamd[0,j] * T1y[j] for j in DMU) - SO[0,0] == T1y[o])    model.addConstr(quicksum(lamd[1,j] * T2y[j] for j in DMU) - SO[1,0] == T2y[o])    model.addConstr(quicksum(lamd[2,j] * T3y[j] for j in DMU) - SO[2,0] == T3y[o])    model.addConstr(quicksum(lamd[3, j] * T4y[j] for j in DMU) - SO[3, 0] == T4y[o])    #free link constraint Eq#(2)    model.addConstr(quicksum(Z12[j] *lamd[0,j] for j in DMU) +SL[0, 0]== Z12[o])    model.addConstr(quicksum(Z23[j] * lamd[1,j] for j in DMU) +SL[1, 0]== Z23[o])    model.addConstr(quicksum(Z34[j] * lamd[2, j] for j in DMU)+SL[2, 0] == Z34[o])    model.addConstr(quicksum(Z45[j] * lamd[3, j] for j in DMU) +SL[3, 0]== Z45[o])    # #fixed link case    # model.addConstr(Z12[o] == quicksum(Z12[j] * lamd[1,j] for j in DMU))    # model.addConstr(Z12[o] == quicksum(Z12[j] * lamd[0, j] for j in DMU))    # model.addConstr(Z23[o] == quicksum(Z23[j] * lamd[1, j] for j in DMU))    # model.addConstr(Z23[o] == quicksum(Z23[j] * lamd[2,j] for j in DMU))    # model.addConstr(quicksum(lamd[0,j] for j in DMU) == 1)    # model.addConstr(quicksum(lamd[1,j] for j in DMU) == 1)    # model.addConstr(quicksum(lamd[2, j] for j in DMU) == 1)    model.update()    model.optimize()    if model.solCount > 0:        print("objective value (Theta) = %0.3f "% model.objVal)    else:        print("solution status = ", model.Status)    E[o] = "The efficiency of DMU %s:%4.3g" % (o, model.objVal) #free link case    # for i in model.getVars():    #     #l[r][i]= "The lamda and effiency of DMU %s: %0.3f"(i.varName, i.x)    #     print("%s %0.3f"%(i.varName, i.x))#x get the lamda values and efficeincy score    for t in range(Terms):        for j in DMU:            L[o]= " %s %0.3f"%(lamd[t, j].varName, lamd[t, j].x)            print(L[o]) #lamda    SO_sol= model.getAttr('x',SO )    print("SO_sol",SO_sol)    SI_sol = model.getAttr('x',SI)    print("SI_sol",SI_sol)    E_term1[o] = "%0.3f" % (1 - (SI_sol[0, 0] / T1x[o]))    E_term2[o] = "%0.3f" % (1 - (SI_sol[1, 0] / T2x[o]))    E_term3[o] = "%0.3f" % (1 - (SI_sol[2, 0] / T3x[o]))    E_term4[o] = "%0.3f" % (1 - (SI_sol[3, 0] / T4x[o]))    print("Term 1 score:", E_term1[o])    print("Term 2 score:",E_term2[o])    print("Term 3 score:",E_term3[o])    print("Term 4 score:", E_term4[o])    #    # for r in range(N3O):    #     SO[2, r] = "%s %0.3f" % (SI[2, r].varName, SI[2, r].x)    #     print(SO[2, r])    #    # for i in range(N1I):    #     SI[0, i] = "%s %0.3f" % (SI[0, i].varName, SI[0, i].x )    #     print(SI[0, i])    #    # for i in range(N2I):    #     SI[1, i] = "%s %0.3f" % (SI[1, i].varName, SI[1, i].x)    #     print(SI[1, i])    #    # for i in range(N3I):    #     SI[2, i] = "%s %0.3f" % (SI[2, i].varName, SI[2, i].x)    #     print(SI[2, i])    print("------------------------")for o in DMU:    print(E[o])