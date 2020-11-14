%% Nasa Curve Fit Program

%{
Mech 447 Project 1 Part 1
Louis Bourque 260714602
Finds Adiabatic flame temperature through solving Nasa Curves given
%}

%% Setup
clear
clc

R = 8.314; %KJ/kmolk-K
syms T; %equation will solve for Temp, setup as variable for later

% NASA CEA tables
NASA_CEA;


%formation energy from Table A-26 Cengel % Boles
hf_co = -110530; %kJ/kmol
hf_co2 = -393520; %kJ/kmol
hf_o2 = 0; %not used, but kept in principle


%Reference enthalpy from Table A-21 Cengel % Boles
href_co2 = 9364; %kJ/kmol
href_o2 = 8682; %kJ/kmol
href_co = 8669; %kJ/kmol


%Reference H(o) for NASA curvefits
h0_CO2 = - 402875;
h0_O2 = - 8680;
h0_CO = - 119206;


% for 1000 < T_expected < 6000 K (CO2)

CO2_a1 = 1.176962419*10^5;
CO2_a2 = -1.788791477*10^3;
CO2_a3 = 8.291523190;
CO2_a4 = -9.223156780*10^-5;
CO2_a5 = 4.863676880*10^-9;
CO2_a6 = -1.891053312*10^-12;
CO2_a7 = 6.330036590*10^-16;
CO2_b1 = -3.908350590*10^4;
CO2_b2 = -2.652669281*10^1;


% 1000 < T_expected < 6000 K (CO)


CO_a1 = 4.619197250*10^5;
CO_a2 = -1.944704863*10^3;
CO_a3 = 5.916714180;
CO_a4 = -5.664282830*10^-4;  
CO_a5 = 1.398814540*10^-7;
CO_a6 = -1.787680361*10^-11; 
CO_a7 = 9.620935570*10^-16; 
CO_b1 = -2.466261084*10^3;
CO_b2 = -1.387413108*10^1;
  
% 1000 < T_expected < 6000 K (O2)

O2_a1 = -1.037939022*10^6;
O2_a2 = 2.344830282*10^3;
O2_a3 = 1.819732036;
O2_a4 =  1.267847582*10^-3; 
O2_a5 = -2.188067988*10^-7;
O2_a6 = 2.053719572*10^-11;
O2_a7 = -8.193467050*10^-16;
O2_b1 = -1.689010929*10^4;
O2_b2 = 1.738716506*10^1;

%% Solve
phi_array = .5:.1:2;
x = zeros(1,length(phi_array));
Q_table = zeros(1,length(phi_array));
T_af = zeros(1,length(phi_array));

for k = 1 : length(phi_array)

%three cases for phi result in different excess products
phi = phi_array(k);

% Using NASA thermofit equations to solve conservation equation
if phi < 1
   Q = (phi*hf_co - phi*hf_co2 + phi*href_co2 + ((1-phi)/2)*href_o2);
   
   eqn = (phi*R*T*(-CO2_a1*T^-2 + CO2_a2*log(T)*T^-1 + CO2_a3 + CO2_a4*T/2 +...
        ...
        CO2_a5*(T^2)/3 + CO2_a6*(T^3)/4 + CO2_a7*(T^4)/5 + CO2_b1/T)) +...
        ...
        ((1-phi)/2)*R*T*(-O2_a1*T^-2 + O2_a2*log(T)*T^-1 + O2_a3 +...
        ...
        O2_a4*T/2 + O2_a5*(T^2)/3 + O2_a6*(T^3)/4 + O2_a7*(T^4)/5 +...
        ...
        O2_b1/T) == Q + phi*h0_CO2 + ((1-phi)/2)*h0_O2;
   
elseif phi == 1
    Q = (hf_co - hf_co2 + href_co2);
    
    eqn = (R*T*(-CO2_a1*T^-2 + CO2_a2*log(T)/T + CO2_a3 + CO2_a4*T/2 +...
        ...
        CO2_a5*(T^2)/3 + CO2_a6*(T^3)/4 + CO2_a7*(T^4)/5 + CO2_b1/T))  == Q + h0_CO2;

else
   Q = (phi*hf_co - hf_co2 + href_co2 - (phi-1)*hf_co + (phi-1)*href_co);
    
   eqn = (R*T*(-CO2_a1*T^-2 + CO2_a2*log(T)/T + CO2_a3 + CO2_a4*T/2 +...
        ...
        CO2_a5*(T^2)/3 + CO2_a6*(T^3)/4 + CO2_a7*(T^4)/5 + CO2_b1/T)) +...
        ...
        ((phi-1)*R*T*(-CO_a1*T^-2 + CO_a2*log(T)*T^-1 + CO_a3 +...
        ...
        CO_a4*T/2 + CO_a5*(T^2)/3 + CO_a6*(T^3)/4 + CO_a7*(T^4)/5 +...
        ...
        CO_b1/T))== Q + h0_CO2 + (phi-1)*h0_CO;
end
    
x(k) = phi;
% Sets up Table for later display
Q_table(k) = Q;
T_af(k) = vpasolve(eqn,T);
end

% Displays found values in Table
Table = table(x(:),T_af(:),Q_table(:));
Table.Properties.VariableNames = {'Fuel Air Ratio' 'Adiabatic Temperature (K)' 'Heat(Total H_at)'}

%Plots found temperature vs calculated temperatures from NASA CEA program
figure(1)
grid on
hold on

plot(x, NASA_complete,'m')
plot(x, T_af,'--b')

xlabel('FA ratio')
ylabel('Temperature(K)')
title('Adiabatic Flame Temperature with varying fuel-to-air ratio')
legend('NASA CEA','T Calculated')


