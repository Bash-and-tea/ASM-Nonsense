void main() {
	__asm__ (
		"movl $1, %eax;\n"
		"movl $1, %ebx;\n"
		"leal 16(%eip), %esi;\n"
		"movl $13, %edx;\n"
		"syscall;\n"
		"movl $60,%eax;\n"
		"xorl %ebx,%ebx; \n"
		"syscall;\n"
		"message: .ascii \"Hello World!\\n\";"
	);
}