clear all
close all
clc

F = 1; %figure at end displayed or not
P = 180*ones(1,65); %for adjusting the quadrant

Tag = 'SiSi_interface';
Num_datapoints = 6;

for Order = 1:Num_datapoints 

% read the data of background noise
prefix = {'01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21'};   
name_B = ['Si_Ref00_',prefix{Order},'.txt'];
[freq_B,t_B,c_B,cos_B,sin_B] = textread(name_B,'%f %f %f %f %f');

% read the data of reference
name_R = ['Si_Ref_',num2str(Order),'.txt'];
[freq_R,t_R,c_R,cos_R,sin_R] = textread(name_R,'%f %f %f %f %f');
freq_R = freq_R/10^6; %in MHz

%remove the background noise from reference, and calculate phase
phase_RB = atan2(sin_R-sin_B,cos_R-cos_B);
phase_RB = phase_RB./pi*180;
%%
figure;
subplot(2,3,1)
semilogx(freq_R,phase_RB);

% remove the discontinuity in calculated angles
phase_RB = link(phase_RB);
subplot(2,3,2)
semilogx(freq_R,phase_RB,'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
title('Reference Phase','fontsize',15);

% read the data of signal/sample
name_S = ['Si_Signal_',num2str(Order),'.txt'];
[freq_S, t_S, c_S,cos_S,sin_S] = textread(name_S,'%f %f %f %f %f');
freq_S = freq_S/10^6;

% remove the noise from signal and calculate phase
phase_SB = atan2(sin_S-sin_B,cos_S-cos_B);
phase_SB = phase_SB./pi*180;

subplot(2,3,3)
semilogx(freq_S,phase_SB);
phase_SB = link(phase_SB);

subplot(2,3,4)
semilogx(freq_S,phase_SB,'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
title('Measured Phase','fontsize',15);

subplot(2,3,5)
hold on
semilogx(freq_R,phase_RB,'o',freq_S,phase_SB,'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
legend({'reference','signal'},'fontsize',15);

% calculate the final phase attributed to the sample as signal minus ref,
% both corrected for the bkg. Additional correction for pi difference in
% phase is added (quadrature adjustment)
phase = phase_SB - phase_RB + P(Order);

subplot(2,3,6)
semilogx(freq_S(1:end-1),link(phase(1:end-1)),'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);
title('Corrected Sample Phase','fontsize',15);

figure
plot(freq_S(1:end-1),link(phase(1:end-1)),'o','linewidth',1.5);
xlabel('Modulated Frequency [MHZ]','fontsize',15);
ylabel('Phase [deg]','fontsize',15);

set(gcf,'position',[200 200 1200 600]);
Phase_Sample{Order} = link(phase);
Frequency_Sample{Order} = freq_S;

frequencyData = Frequency_Sample{Order};
phaseData = Phase_Sample{Order};

% Combine the data into a matrix
dataTable = table(frequencyData, phaseData, 'VariableNames', {'Frequency', 'Phase'});
filename = ['Results_', Tag, '_', num2str(Order), '.csv'];
writetable(dataTable, filename);

end

save(['Phase_',Tag],['Phase_Sample']);
save(['Frequency_',Tag],['Frequency_Sample']);


if F == 1
    figure
    hold on
    for i = 1:Num_datapoints
        semilogx(Frequency_Sample{i},Phase_Sample{i},'.','MarkerSize',12,'linewidth',1.5);
    end
    xlabel('Frequency [MHZ]');
    ylabel('Phase[Deg]');
    set(gca,'fontsize',15);
    box on
    set(gca,'fontweight','bold');
    legend({'1st','2nd','3rd', '4th','5th', '6th'}); %,'
    title(Tag);
    saveas(gca,['FDTR_',Tag,'.png']);
    saveas(gca,['FDTR_',Tag,'.fig']);
end

% figure;
% plot(freq1,a1,'o','linewidth',1.5)
% hold on
% plot(freq1,a2,'o','linewidth',1.5)
% figure;
% plot([10:4:150],P1,'o','linewidth',1.5);
% hold on
% plot([10:2:150],P1_2(1:71),'o','linewidth',1.5);
% legend({'Reference of this measurement','Data before'});
% xlabel('Frequency [MHZ]','fontsize',15);
% ylabel('Phase [deg]');