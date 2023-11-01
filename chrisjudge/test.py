import subprocess
import time

def checkfile(file,question):
    testinput=question[5].split("|&|")
    testoutput=question[6].split("|&|")
    success=True
    runtime=time.time()
    result="SU"
    response=""
    timelimit=100 # 設定執行時間限制(s)

    for i in range(len(testinput)):
        inputruntime=time.time()
        try:
            output=subprocess.run("php -d memory_limit=128M "+str(file),input=str(testinput[i]),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timelimit,universal_newlines=True) # 執行PHP程式,輸入測試資料，並設定時間限制

            outputtext=output.stdout.rstrip() # 獲取輸出結果

            expectedoutput="".join(testoutput[i].split("\n"))
            actualoutput="".join(outputtext.split("\n"))

            print("expectedoutput: "+expectedoutput)
            print("actualoutput: "+actualoutput)

            # 看記憶體有沒有爆掉
            if output.returncode!=0:
                success=False
                result="MF"
                response=f"{response}\n test_{i+1} failed memory overload,\n max memory: 128MB"

            # 比對輸出結果
            elif actualoutput!=expectedoutput:
                success=False
                result="RF"
                response=f"{response}\n test_{i+1} failed respound failed,\n input: {testinput[i]},\n expectedoutput: {expectedoutput},\n actualoutput: {actualoutput},"

            # 超時
            elif time.time()-inputruntime>int(question[7]):
                success=False
                result="OT"
                response=f"{response}\n test_{i+1} failed overtime,\n input: {testinput[i]},\n expectedoutput: {expectedoutput},\n actualoutput: {actualoutput},"

            else:
                response=f"{response}\n test_{i+1} success,\n input: {testinput[i]},\n expectedoutput: {expectedoutput},\n actualoutput: {actualoutput},"

        except subprocess.TimeoutExpired:
            success=False
            runtime=">100s"
            result="OT"
            response=f"{response}\n test_{i+1} failed overtime,\n input: {testinput[i]},\n expectedoutput: {expectedoutput},\n actualoutput: N/A,"

    if success:
        runtime=time.time()-runtime

    return {
        "success": success,
        "response": response, # 回傳所有測試的輸出
        "runtime": runtime, # 回傳執行時間
        "result": result
    }