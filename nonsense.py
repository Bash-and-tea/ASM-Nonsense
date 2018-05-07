import re
import subprocess
import math

def write_template(message, len_mess):
	with open('nonsense_template.c', 'w') as fout:
		fout.write(r'void main() {' + '\n' +
				   r'	__asm__ (' + '\n' +
				   r'		"movl $1, %eax;\n"' + '\n' +
				   r'		"movl $1, %ebx;\n"' + '\n' +
				   r'		"leal 16(%eip), %esi;\n"' + '\n' +
				   r'		"movl $' + str(len_mess) + r', %edx;\n"' + '\n' +
				   r'		"syscall;\n"' + '\n' +
				   r'		"movl $60,%eax;\n"' + '\n' +
            	   r'		"xorl %ebx,%ebx; \n"' + '\n' +
            	   r'		"syscall;\n"' + '\n' +
            	   r'''		"message: .ascii \"''' + str(message) + r'''\\n\";"''' + '\n' + 
				   r'	);' + '\n' +
				   r'}')
		fout.close()
	return

def do_gcc1(filename):
	subprocess.run(["gcc -Wall " + filename + " -o nonsense"], shell=True)
	return

def do_gcc2(filename):
	subprocess.run(["gcc -Wall " + filename + " -o obs"], shell=True)
	return

def disas():
	subprocess.run(["gdb " + '-ex "disas main" ' + '-ex "quit"' + " ./nonsense" + " > numbytes.txt"], shell=True)
	return

def int_arr_dump(main_len):
	subprocess.run(["gdb" + ' -ex "x/' + str(math.ceil(float(main_len) / 4.0)) + 'dw main"' + ' -ex "quit"' + " ./nonsense" + " > dump.txt"], shell=True)

def call_gdb():
	do_gcc1('nonsense_template.c')
	disas()
	text_list = []
	text_list = open('numbytes.txt', 'r').read().split('\n')
	index = 0
	for line in text_list:
		if line == "End of assembler dump.":
			index -= 1
			break
		else:
			index += 1
	keyline = list(text_list[index])
	index = 0
	for char in keyline:
		if char == "+":
			first = index + 1
			second = index + 2
			break
		else:
			index += 1
	main_len = float(str(keyline[first]) + str(keyline[second]))
	int_arr_dump(main_len)
	return	

def dissect():
	cmdarray = []
	dump = open('dump.txt', 'r').read().split('\n')
	cmdlines = filter(lambda x: re.search(r"<main+", x), dump)
	for cmdline in cmdlines:
		operable = list(cmdline)
		operable.append('\t')
		# print(operable)
		c = 0
		tempnum = ''
		for char in operable:
			if char == ':' and operable[(c + 1)] == '\t':
				start = c + 2
			else:
				c += 1
		operable = operable[start:]
		for char in operable:
			# if char == '-':
			# 	tempnum += char
			# elif type(char) == type(int()):
			# 	tempnum += char
			if not (char == '\t'):
				tempnum += char
				# print(tempnum)
			else:
				# print(tempnum)
				cmdarray.append(int(tempnum))
				tempnum = ''
	return cmdarray

def writeprog(cmdarray):
	with open('obs.c', 'w') as comp:
		comp.write(r'const int main[] = {' + '\n')
		for number in cmdarray:
			comp.write(str(number) + ', ')
		comp.write('};\n')
		comp.close()
	do_gcc2('obs.c')
	return

def main():
	message = input("What message would you like to obfuscate?: ")
	len_mess = len(message) + 1
	write_template(message, len_mess)
	call_gdb()
	commands = dissect()
	writeprog(commands)
	print("Build complete!")
	subprocess.run(['./obs'], shell=True)
	print("Execution complete!")

if __name__ == "__main__":
	main()

