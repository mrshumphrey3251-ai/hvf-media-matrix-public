@echo off 
REM HVF SYSTEM KINETIC GUILLOTINE 
REM Architect: Mr. Humphrey 
set TARGET_IP=10.19.193.194 
set TARGET_USER=mrshumphrey3251 
echo [HVF SYSTEM] Initiating Kinetic Guillotine strike on %%TARGET_IP%%... 
ssh -t %%TARGET_USER%%@%%TARGET_IP%% "sudo shutdown -h now" 
echo [HVF SYSTEM] Strike complete. Linux engine terminated. 
pause 
