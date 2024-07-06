import subprocess
import time

def checkfile(file,question):
    testinput=question[5].split("|&|")
    testoutput=question[6].split("|&|")
    success=True
    runtime=time.time()
    result="SU"
    response=""
    timelimit=20 # 設定執行時間限制(s)

    for i in range(len(testinput)):
        inputruntime=time.time()
        try:
            output=subprocess.run("php -d memory_limit=128M "+str(file),input=str(testinput[i]),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timelimit,universal_newlines=True) # 執行PHP程式,輸入測試資料，並設定時間限制
            outputruntime=time.time()

            outputtext=output.stdout.rstrip() # 獲取輸出結果

            expectedoutput="".join(testoutput[i].split("\n")).strip()
            actualoutput="".join(outputtext.split("\n")).strip()

            # print("expectedoutput: "+expectedoutput)
            # print("actualoutput: "+actualoutput)

            # 看記憶體有沒有爆掉
            if output.returncode!=0:
                success=False
                if result=="SU":
                    result="MF"
                response=f"{response}test_{i+1} failed memory overload\nmax memory: 128MB\n"

            # 比對輸出結果
            elif actualoutput!=expectedoutput:
                success=False
                if result=="SU":
                    result="RF"
                response=f"{response}test_{i+1} failed respound failed\ninput:\n{testinput[i]}\nexpectedoutput: {expectedoutput}\nactualoutput: {actualoutput}\n"

            # 超時
            elif int(question[7])<round(outputruntime-inputruntime): # [BUG]這個round是偷吃步解法
                success=False
                if result=="SU":
                    result="OT"
                response=f"{response}test_{i+1} failed overtime\ninput:\n{testinput[i]}\nexpectedoutput: {expectedoutput}\nactualoutput: {actualoutput}\n"

            else:
                response=f"{response}test_{i+1} success\ninput:\n{testinput[i]}\nexpectedoutput: {expectedoutput}\nactualoutput: {actualoutput}\n"

        except subprocess.TimeoutExpired:
            success=False
            runtime=">100s"
            result="OT"
            response=f"{response}test_{i+1} failed overtime\ninput:\n{testinput[i]}\nexpectedoutput: {expectedoutput}\nactualoutput: N/A\n"

    return {
        "success": success,
        "response": response, # 回傳所有測試的輸出
        "runtime": time.time()-runtime, # 回傳執行時間
        "result": result
    }