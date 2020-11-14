%% Project 2 Main - Mech 447
%{
Chemical Kinetics + Thermal Explosion for CO/O2
By: Louis Bourque - 260714602
%}

clc
clear

% Call known CEA_results to check later
CEA_results


%% Part 1

% Involves constant reaction coefficients, so slight tweak to ODEsolver
Project2_Part1

%% Part 2

% span for ODE's for Part 1 and 2
tspan = [0:.00001:.015];

[full_per2,t] = Oxidation(1,298,1500,0,tspan);

Table2 = table(CEA_out2(:),full_per2(end,1:4)');
Table2.Properties.VariableNames = {'CEA' 'Calculated'};
Table2.Properties.RowNames = {'CO' 'CO2' 'O' 'O2'}

% Plot mole Fractions
figure(4)
grid on
hold on
plot(t,full_per2(:,1:4))
yline(CEA_out2(1),'b--','CO Equilibrium')
yline(CEA_out2(2),'r--','CO2 Equilibrium')
yline(CEA_out2(3),'k--','O Equilibrium')
yline(CEA_out2(4),'m--','O2 Equilibrium')
legend('CO', 'CO2', 'O', 'O2')
title('Carbon Monoxide Oxidation in Constant Volume Reaction')
xlabel('Time (s)')
ylabel('Molar Fractions')
hold off;

% Plot Temperature
figure(5)
grid on
hold on
plot(t,full_per2(:,6))
title('Temperature of Carbon Monoxide Oxidation in Constant Volume')
xlabel('Time (s)')
ylabel('Temperature (K)')
hold off

% Plot Pressure
figure(6)
grid on
hold on
plot(t,full_per2(:,7))
title('Pressure of Carbon Monoxide Oxidation in Constant Volume')
xlabel('Time (s)')
ylabel('Pressure (atm)')
hold off

% Global Reaction Time Plotting

% Setup matrixes
rxn_span = 1200:100:2000;
rxn_time = zeros(length(rxn_span),2);
tspan = [0:1e-5:.2];


for j = 1:numel(rxn_span)
    % Solve Temperature Graph for given T_ini
    [rxn_per,t_rxn] = Oxidation(1,298,rxn_span(j),0,tspan);
    
    % Initialize constants for checks, starting from end of reaction
    
    T_rxn = (rxn_per(end,6) - rxn_per(1,6))/2 + rxn_per(1,6);
    
    % Find Temp and Time when steady state is lost by moving left across
    % reaction
    [val, indx] = min(abs(rxn_per(:,6)-T_rxn));
    
    % Matrix keeps [ln(1/(t/2)), 1/T_max]
    rxn_time(j,1) = 1/rxn_per(1,6);
    rxn_time(j,2) = log(1/(t_rxn(indx)));
    
end

% Plot 1/T and ln(1/tau)
figure(7)
plot(rxn_time(:,1),rxn_time(:,2));
grid on;
hold on;

% Line of Best Fit
coefficients = polyfit(rxn_time(:,1), rxn_time(:,2), 1);
Ea = -coefficients(1)*R;

xFit = linspace(min(rxn_time(:,1)), max(rxn_time(:,1)), 1000);
yFit = polyval(coefficients , xFit);
plot(xFit, yFit, 'k--', 'LineWidth', 1);

% Line of Best Fit Caption

xl = xlim;
yl = ylim;
xt = 0.4 * (xl(2)-xl(1)) + xl(1);
yt = 0.8 * (yl(2)-yl(1)) + yl(1);
caption = sprintf('y = %f x + %f',coefficients(1),coefficients(2));
text(xt, yt, caption, 'FontSize', 12, 'Color', 'k');

xt2 = 0.55 * (xl(2)-xl(1)) + xl(1);
yt2 = 0.65 * (yl(2)-yl(1)) + yl(1);
caption = sprintf('Ea = %f kJ/kmol',Ea);
text(xt2, yt2, caption, 'FontSize', 11, 'Color', 'k');

legend('Actual','Best Fit')
xlabel('Inverse Temperature (1/K)')
ylabel('Global Reaction Time ln(1/s)')
title('Global Effective Activation Energy Plot')
hold off



%% Part 3
V = 1e-6; %m3
tspan = [0:.01:6];

% Example calculation for one temperature along with molar concentrations
[full_per3,t] = Oxidation(V,298,1145,1,tspan);

figure(8)
hold on
grid on
plot(t(:),full_per3(:,1:4))
xlabel('Time (s)')
ylabel('Molar Percentages')
title('Molar Percentages of CO Oxydation at thermal runaway T=1145K')
legend('CO', 'CO2', 'O', 'O2')

for i = 0:5
[full_per4,t] = Oxidation(V,298,1140+i,1,tspan);

% Plot temperature outputs for different oil temperatures
figure(9)
hold on
grid on
plot(t(:),full_per4(:,6))

% Plot CO concentrations at different oil temperatures
figure(10)
hold on
grid on
plot(t(:),full_per4(:,2))
end

% Label graphs outside of for loop to avoid errors
figure(9)
xlabel('Time (s)')
ylabel('Temperature (K)')
title('Temperature of CO Oxydation near thermal runaway')
legend('1140', '1141', '1142', '1143', '1144', '1145')

figure(10)
xlabel('Time (s)')
ylabel('Molar Percentages')
title('Molar Percentages of CO2 during CO Oxydation near Thermal Runaway')
legend('1140', '1141', '1142', '1143', '1144', '1145')