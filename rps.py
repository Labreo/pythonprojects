#
import random
draw=0
win=0
loss=0
s=''
print("--Rock Paper Scissor--\n")
print("Play by entering Rock,Paper or Scissor.Type SCORE to check your stats.Type QUIT to exit the program.\n")
while True:
    
    s=input("Make your choice:")
    s=s.lower()
    if s not in ['quit', 'rock', 'paper', 'scissor', 'score']:
      print('Invalid command! Try again.')
      continue
    if s=="quit":
        print('\nThanks for playing!:)')
        break
    response=['rock','paper','scissor']
    comp=random.choice(response)
    if s==comp:
     print(f"\nThe computer picked {comp}.It is a draw!")
     draw+=1
    if s=='rock' and comp=='paper':
     print(f"\nThe computer picked {comp}.You lost!\n")
     loss+=1
    if s=='rock' and comp=='scissor':
     print(f"\nThe computer picked {comp}.You won!\n")
     win+=1
    if s=='paper' and comp=='rock':
     print(f"\nThe computer picked {comp}.You won!\n")
     win+=1
    if s=='paper' and comp=='scissor':
     print(f"\nThe computer picked {comp}.You lost!\n")
     loss+=1
    if s=='scissor' and comp=='rock':
     print(f"\nThe computer picked {comp}.You lost!\n")
     loss+=1
    if s=='scissor' and comp=='paper':
     print(f"\nThe computer picked {comp}.You won!\n")
     win+=1
    if s=='score':
      print(f'You won a total of {win} times.You lost a total of {loss} times and you drawed a total of {draw} times in this session.\n')






    
    

