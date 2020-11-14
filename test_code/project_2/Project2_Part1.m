%% Project 2 - Mech 447
%{
Chemical Kinetics + Thermal Explosion for CO/O2 - PART 1
By: Louis Bourque - 260714602
%}

%% Setup - Part 1
clear
clc

% Call known CEA_results to check later
CEA_results

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
T = 3000; % K
R = 8.314; % J mol^-1 K^-1
V = 1; % m^3

% Find initial moles of CO and O2 at specified volume and temperature
CO_ini = (2/3)*(1000/22.4)*(273.15/T);
O2_ini = (1/3)*(1000/22.4)*(273.15/T);
n_init = CO_ini + O2_ini;

% Initial mole values of [CO CO2 O O2 M]
init = [CO_ini 0 0 O2_ini (CO_ini + O2_ini)];

% PV = nRT
P_init = 1000*R*(n_init/1000)*T;

% Matrixes of reaction values
A = [A_1; A_2; A_3];
n = [n_1; n_2; n_3];
Ea = [Ea_1; Ea_2; Ea_3];

% NASA Thermofits solver in form [hf, H, So]
[Fit] = thermofit(T);

%% Finding Reactions rates

Kf = zeros(3,1);

% Find K forward (Kf)
for i = 1:3
    Kf(i) = A(i)*T^n(i)*exp(-Ea(i)/(R*T));
end

% Finding Kc


    % g_star = H - T*so
    g_star = zeros(4,1);

    for i = 1:length(g_star)
        g_star(i) = Fit(i,2) - T*Fit(i,3);
    end

    % Gibbs of each reaction
    dG = zeros(3,1);

    dG(1) = g_star(2) - g_star(1) - g_star(3);
    dG(2) = g_star(2) + g_star(3) - g_star(1) - g_star(4);
    dG(3) = g_star(4) - 2*g_star(3);

    % Solve Kp
    for i = 1:length(dG)
       Kp(i) = exp(-dG(i)/(R*T));
    end
    
% Setup mole change for each reaction
dn = [-1; 0; -1];

% Kc = Kp / (RT/p_init)^dn
Kc = zeros(3,1);

for i = 1:length(Kp)
   Kc(i) = Kp(i) / ((R*T/101325)^dn(i)); 
end

% Backwards reaction is Kf/Kc
Kb = Kf./Kc;

%% ODE Solving

% Solve ODE with only forward reactions
[t,Compfwd] = ODEsolver1(Kf(1),Kf(2),Kf(3),0,0,0,init);

for i = 1:length(Compfwd)
    fdw_per(i,:) = Compfwd(i,:) / Compfwd(i,5);
end

figure(1);
hold on;
grid on;

% Early equilibrium to .25e-4 seconds for transient state
plot(t(1:600),fdw_per(1:600,1:4))
yline(CEA_out1(1),'b--','CO Equilibrium')
yline(CEA_out1(2),'r--','CO2 Equilibrium')
yline(CEA_out1(3),'k--','O Equilibrium')
yline(CEA_out1(4),'m--','O2 Equilibrium')
legend('CO', 'CO2', 'O', 'O2')
title('Transient Composition of Carbon Monoxide Oxidation - Fwd Reactions only')
xlabel('Time (s)')
ylabel('Molar Fractions')

hold off



figure(2);
hold on;
grid on;

% Early equilibrium to .25e-4 seconds for transient state
plot(t,fdw_per(:,1:4))
yline(CEA_out1(1),'b--','CO Equilibrium')
yline(CEA_out1(2),'r--','CO2 Equilibrium')
yline(CEA_out1(3),'k--','O Equilibrium')
yline(CEA_out1(4),'m--','O2 Equilibrium')
legend('CO', 'CO2', 'O', 'O2')
title('Composition of Carbon Monoxide Oxidation - Fwd Reactions only')
xlabel('Time (s)')
ylabel('Molar Fractions')

hold off

% Solve ODE with forward and backwards reactions
[t,Comp_full] = ODEsolver1(Kf(1),Kf(2),Kf(3),Kb(1),Kb(2),Kb(3),init);

for i = 1:length(Comp_full)
    full_per(i,:) = Comp_full(i,:) / Comp_full(i,5);
end

figure(3);
grid on;
hold on;

plot(t,full_per(:,1:4))
yline(CEA_out1(1),'b--','CO Equilibrium')
yline(CEA_out1(2),'r--','CO2 Equilibrium')
yline(CEA_out1(3),'k--','O Equilibrium')
yline(CEA_out1(4),'m--','O2 Equilibrium')
legend('CO', 'CO2', 'O', 'O2')
title('Composition of Carbon Monoxide Oxidation')
xlabel('Time (s)')
ylabel('Molar Fractions')
hold off;


Table1 = table(CEA_out1(:),full_per(end,1:4)',fdw_per(end,1:4)');
Table1.Properties.VariableNames = {'CEA' 'Full Reactions' 'Fwd Only'};
Table1.Properties.RowNames = {'CO' 'CO2' 'O' 'O2'}
