def largest_number(numbers):
    selected_list=[]
    result = ""
    for num in numbers :   
        string_number = str(num)

        if len(selected_list) ==0 :
            selected_list.append(string_number)
        elif len(selected_list) == 1:
            if first_num(selected_list[0])<first_num(string_number):
                    selected_list.insert(0, string_number)
            elif first_num(selected_list[0])==first_num(string_number):
                if len(selected_list[0])>len(string_number):
                    selected_list.insert(0, string_number)
                else :
                    selected_list.append(string_number)
            else :
                selected_list.append(string_number)
        else :  
            for i in range(len(selected_list)) :
                print(first_num(selected_list[i]))
                print(first_num(string_number))
                print(i)
                if first_num(selected_list[i])<first_num(string_number):
                    selected_list.insert(i, string_number)
                    break
                elif first_num(selected_list[i])==first_num(string_number):
                    if len(selected_list[i])>len(string_number):
                        selected_list.insert(i, string_number)
                        break
                    elif len(selected_list[i])==len(string_number):
                        if int(str(selected_list[i])[1])<int(str(string_number)[1]):
                            selected_list.insert(i, string_number)
                            break
            if string_number not in selected_list :
                selected_list.append(string_number)

    for elem in selected_list:
        result = compare(result, elem)
    return result



def first_num(number):
    return int(number[0])
def compare(a,b):
    res = ""
    if int(str(a)+str(b))>= int(str(b)+str(a)):
        res= str(a)+str(b)
    else :
        res =str(b)+str(a)
    return res
test = [11, 9, 31, 7, 33, 1, 3]
print(largest_number(test))
print("973331111")