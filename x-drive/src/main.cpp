#include "main.h"

#define FLPORT 11
#define FRPORT 1
#define BLPORT 20
#define BRPORT 10
#define DRIVEGEARSET pros::E_MOTOR_GEARSET_18

pros::Motor fl(FLPORT, DRIVEGEARSET, 0), // m1
			fr(FRPORT, DRIVEGEARSET, 1), // m2
			bl(BLPORT, DRIVEGEARSET, 0), // m4
			br(BRPORT, DRIVEGEARSET, 1); // m3

pros::Controller master(pros::E_CONTROLLER_MASTER);

// Clamp returns the input if it is within the min & max range, otherwise it returns min if it is below or max if above
int clamp(int min, int max, int x) {
	if (x > max) {
		return(max);
	} else if (x < min) {
		return(min);
	} else {
		return(x);
	}
}

// Runs each wheel individually to check that the motor setup was correct, uses the dpad and X & B buttons to control each wheel
void calibrateWheels() {
	if (master.get_digital(pros::E_CONTROLLER_DIGITAL_UP)) { // m1
		fl = 50;
	} else {
		fl = 0;
	}
	if (master.get_digital(pros::E_CONTROLLER_DIGITAL_DOWN)) { // m4
		bl = 50;
	} else {
		bl = 0;
	}
	if (master.get_digital(pros::E_CONTROLLER_DIGITAL_X)) { // m2
		fr = 50;
	} else {
		fr = 0;
	}
	if (master.get_digital(pros::E_CONTROLLER_DIGITAL_B)) { // m3
		br = 50;
	} else {
		br = 0;
	}
}

// Calculates and sets wheel velocities for the xdrive
void xDrive() {
	int Lx = master.get_analog(ANALOG_LEFT_X); // x axis of translation control
	int Ly = master.get_analog(ANALOG_LEFT_Y); // y axis of translation control
	int Rx = master.get_analog(ANALOG_RIGHT_X); // rotation axis control

	// Velocity calc for each motor (can work for motor groups too)
	int vm1 = (Lx + Ly) + Rx;
	int vm2 = (Ly - Lx) - Rx;
	int vm3 = (Lx + Ly) - Rx;
	int vm4 = (Ly - Lx) + Rx;

	// Clamp values
	vm1 = clamp(-127, 127, vm1);
	vm2 = clamp(-127, 127, vm2);
	vm3 = clamp(-127, 127, vm3);
	vm4 = clamp(-127, 127, vm4);

	// Assign Values
	fl = vm1;
	fr = vm2;
	br = vm3;
	bl = vm4;
}


/**
 * Runs initialization code. This occurs as soon as the program is started.
 *
 * All other competition modes are blocked by initialize; it is recommended
 * to keep execution time for this mode under a few seconds.
 */
void initialize() {
	pros::lcd::initialize();
}

/**
 * Runs while the robot is in the disabled state of Field Management System or
 * the VEX Competition Switch, following either autonomous or opcontrol. When
 * the robot is enabled, this task will exit.
 */
void disabled() {}

/**
 * Runs after initialize(), and before autonomous when connected to the Field
 * Management System or the VEX Competition Switch. This is intended for
 * competition-specific initialization routines, such as an autonomous selector
 * on the LCD.
 *
 * This task will exit when the robot is enabled and autonomous or opcontrol
 * starts.
 */
void competition_initialize() {}

/**
 * Runs the user autonomous code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the autonomous
 * mode. Alternatively, this function may be called in initialize or opcontrol
 * for non-competition testing purposes.
 *
 * If the robot is disabled or communications is lost, the autonomous task
 * will be stopped. Re-enabling the robot will restart the task, not re-start it
 * from where it left off.
 */
void autonomous() {}

/**
 * Runs the operator control code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the operator
 * control mode.
 *
 * If no competition control is connected, this function will run immediately
 * following initialize().
 *
 * If the robot is disabled or communications is lost, the
 * operator control task will be stopped. Re-enabling the robot will restart the
 * task, not resume it from where it left off.
 */
void opcontrol() {
	while (true) {
		xDrive();
		// calibrateWheels();

		pros::delay(20);
	}
}
