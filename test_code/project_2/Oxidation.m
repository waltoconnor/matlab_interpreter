function [full_per,t] = Oxidation(V,T_ref,T_heat,Bnry,tspan)
    %% Setup
    
    % Molar Masses
    CO_mm = 28; %g/mol
    O2_mm = 16; %g/mol
    
    % Reaction 1: CO + O + M = CO2 + M
    A_1 = 1.8e-2; % m^6 kmol^-2 s^-1
    n_1 = 0;
    Ea_1 = 9970; % kJ/kmol

    % Reaction 2: CO + O2 = CO2 + O
    A_2 = 2.5e6; % m^3 kmol^-1 s^-1
    n_2 = 0;
    Ea_2 = 200000; % kJ/kmol

    % Reaction 3: O + O + M = O2 + M
    A_3 = 1.2e5; % m^6 kmol^-2 s^-1
    n_3 = -1;
    Ea_3 = 0; % kJ/kmol

    % initialization
    R = 8.314; % J mol^-1 K^-1
    
    
    % Find initial moles of CO and O2 at specified volume and temperature
    CO_ini = (2/3)*V*(1000/22.4)*(273.15/T_ref);
    O2_ini = (1/3)*V*(1000/22.4)*(273.15/T_ref);
    n_init = CO_ini + O2_ini;

    % P with heated reactants
    P_heat = n_init*R*T_heat/V;
    
    % Initial mole values of [CO CO2 O O2 M]
    init = [CO_ini/V 0 0 O2_ini/V n_init/V T_heat P_heat];

    % Matrixes of reaction values
    A = [A_1; A_2; A_3];
    n = [n_1; n_2; n_3];
    Ea = [Ea_1; Ea_2; Ea_3];

    % Reaction rate solving now moved into ODE solver for Part 2
    
    %% ODE Solving

    % Solve ODE with forward and backwards reactions
    [t,Comp_full] = ODEsolver(A,n,Ea,V,Bnry,init,tspan);

    full_per = zeros(length(Comp_full),7);
    
    for i = 1:length(Comp_full)
        % Molar Fractions based on total moles
        full_per(i,1:4) = Comp_full(i,1:4) / Comp_full(i,5);
        % Temperature in K
        full_per(i,6) = Comp_full(i,6);
        % Pressure in atm
        full_per(i,7) = Comp_full(i,7)/101325;
    end

end

