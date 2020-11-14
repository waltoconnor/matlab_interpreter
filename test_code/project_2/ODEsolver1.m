function [t, Comp] = ODEsolver1(Kf_1,Kf_2,Kf_3,Kb_1,Kb_2,Kb_3,init)
%ODESOLVER: Takes reaction rates and initial values as input
    % Returns Composition matrix and total moles (M)
    % Fractions can be found n/M
%{
Setup ODE equations with Compositions in matrix y
This is in form: y = [n_CO, n_CO2, n_O, n_O2, M]'
%}

    tspan = [0:.0001:.3];
    [t,Comp] = ode15s(@(t,y) odefnct(t,y,Kf_1,Kf_2,Kf_3,Kb_1,Kb_2,Kb_3), tspan, init);

    function dydt = odefnct(t,y,Kf_1,Kf_2,Kf_3,Kb_1,Kb_2,Kb_3)
    
    % All functions are a combination of similar variables,simplify
    react_1 = Kf_1*y(1)*y(3)*y(5);
    prod_1 = Kb_1*y(2)*y(5);
    react_2 = Kf_2*y(1)*y(4);
    prod_2 = Kb_2*y(2)*y(3);
    react_3 = Kf_3*y(3)*y(3)*y(5);
    prod_3 = Kb_3*y(4)*y(5);
    
    % Setup actual ODE system with simplified code
    dydt = zeros(5,1);
    dydt(1) = -react_1 - react_2 + prod_1 + prod_2;
    dydt(2) = react_1 + react_2 - prod_1 - prod_2;
    dydt(3) = -react_1 + react_2 - 2*react_3 + prod_1 - prod_2 + 2*prod_3;
    dydt(4) = -react_2 + react_3 + prod_2 - prod_3;
    dydt(5) = dydt(1) + dydt(2) + dydt(3) + dydt(4);
    end
end