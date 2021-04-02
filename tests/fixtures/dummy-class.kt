class MyClass {

	fun func1() {
		val resource = R.drawable.drawable_used_programatically

		val textColor = if(condition) context.getColor(R.color.programatic_1) else context.getColor(R.color.programatic_2)
	}
}