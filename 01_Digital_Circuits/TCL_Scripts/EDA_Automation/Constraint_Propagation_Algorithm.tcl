package require Tcl 8.6

namespace eval TimingConstraint {
    variable variables
    variable domains
    variable constraints
    variable queue

    # Initialize the constraint system
    proc init {} {
        variable variables [dict create]
        variable domains [dict create]
        variable constraints [dict create]
        variable queue [list]
    }

    # Add a timing variable with initial domain
    proc add_variable {name {min 0} {max 100}} {
        variable variables
        variable domains

        dict set variables $name 1
        dict set domains $name [list $min $max]
    }

    # Add timing constraint: A + delay ≤ B
    proc add_constraint {A B {min_delay 0} {max_delay inf}} {
        variable constraints

        set constraint_id "[string map {: _} $A]_to_[string map {: _} $B]"
        dict set constraints $constraint_id [list $A $B $min_delay $max_delay]

        # Add reverse constraint for bidirectional propagation
        set rev_constraint_id "[string map {: _} $B]_to_[string map {: _} $A]"
        if {$max_delay != "inf"} {
            dict set constraints $rev_constraint_id [list $B $A [expr {-$max_delay}] "inf"]
        } else {
            dict set constraints $rev_constraint_id [list $B $A "-inf" "inf"]
        }
    }

    # Constraint propagation function
    proc propagate {} {
        variable domains
        variable constraints
        variable queue

        set changed true
        set iterations 0
        set max_iterations 1000

        while {$changed && $iterations < $max_iterations} {
            set changed false
            incr iterations

            foreach {constraint_id constraint_data} $constraints {
                lassign $constraint_data A B min_delay max_delay

                if {![dict exists $domains $A] || ![dict exists $domains $B]} {
                    continue
                }

                lassign [dict get $domains $A] A_min A_max
                lassign [dict get $domains $B] B_min B_max

                set original_A_min $A_min
                set original_A_max $A_max
                set original_B_min $B_min
                set original_B_max $B_max

                # Forward propagation: A + min_delay ≤ B
                if {$min_delay != "-inf"} {
                    set new_B_min [expr {max($B_min, $A_min + $min_delay)}]
                    if {$new_B_min > $B_min} {
                        dict set domains $B [list $new_B_min $B_max]
                        set changed true
                    }
                }

                # Backward propagation: B - max_delay ≥ A
                if {$max_delay != "inf"} {
                    set new_A_max [expr {min($A_max, $B_max - $max_delay)}]
                    if {$new_A_max < $A_max} {
                        dict set domains $A [list $A_min $new_A_max]
                        set changed true
                    }
                }

                # Update current values after potential changes
                if {$changed} {
                    lassign [dict get $domains $A] A_min A_max
                    lassign [dict get $domains $B] B_min B_max
                }

                # Check for constraint violations
                if {$A_min > $A_max || $B_min > $B_max} {
                    error "Constraint violation detected between $A and $B"
                }

                if {$min_delay != "-inf" && $A_max + $min_delay > $B_max} {
                    error "Minimum delay constraint violated between $A and $B"
                }

                if {$max_delay != "inf" && $A_min + $max_delay < $B_min} {
                    error "Maximum delay constraint violated between $A and $B"
                }
            }
        }

        if {$iterations >= $max_iterations} {
            puts "Warning: Maximum iterations reached without convergence"
        }

        return $iterations
    }

    # Get current domain of a variable
    proc get_domain {variable} {
        variable domains
        if {[dict exists $domains $variable]} {
            return [dict get $domains $variable]
        }
        return {}
    }

    # Display current state
    proc display_state {} {
        variable domains
        variable constraints

        puts "Current Domains:"
        foreach var [dict keys $domains] {
            lassign [dict get $domains $var] min max
            puts "  $var: \[$min, $max\]"
        }

        puts "\nConstraints:"
        foreach {constraint_id constraint_data} $constraints {
            lassign $constraint_data A B min_delay max_delay
            puts "  $A → $B: delay ∈ \[$min_delay, $max_delay\]"
        }
    }
}

# Example usage
proc example_timing_constraints {} {
    TimingConstraint::init

    # Add timing variables (events)
    TimingConstraint::add_variable "clock" 0 10
    TimingConstraint::add_variable "data_in" 2 8
    TimingConstraint::add_variable "data_out" 5 15
    TimingConstraint::add_variable "latch" 3 12

    # Add timing constraints
    TimingConstraint::add_constraint "clock" "data_in" 1 4    ;# clock to data_in delay
    TimingConstraint::add_constraint "data_in" "data_out" 2 6 ;# data_in to data_out delay
    TimingConstraint::add_constraint "clock" "latch" 0 3      ;# clock to latch delay
    TimingConstraint::add_constraint "latch" "data_out" 1 5   ;# latch to data_out delay

    puts "Initial state:"
    TimingConstraint::display_state

    # Perform constraint propagation
    set iterations [TimingConstraint::propagate]

    puts "\nAfter $iterations iterations of propagation:"
    TimingConstraint::display_state

    return [TimingConstraint::get_domain "data_out"]
}


# Precondition checks
proc validate_inputs {variables constraints} {
    # Check for undefined variables in constraints
    foreach constraint $constraints {
        lassign $constraint A B min_delay max_delay
        if {![dict exists $variables $A] || ![dict exists $variables $B]} {
            error "Undefined variable in constraint"
        }
    }

    # Check for valid delay ranges
    foreach constraint $constraints {
        lassign $constraint A B min_delay max_delay
        if {$min_delay > $max_delay} {
            error "Invalid delay range: min > max"
        }
    }
}

# Optimized constraint checking
proc optimized_propagate {} {
    # Use efficient data structures
    set active_constraints [list]

    # Only process constraints with recently changed variables
    while {[llength $active_constraints] > 0} {
        set constraint [lindex $active_constraints 0]
        set active_constraints [lrange $active_constraints 1 end]

        # Process constraint and add affected constraints to queue
        if {[process_constraint $constraint]} {
            lappend active_constraints {*}[get_affected_constraints $constraint]
        }
    }
}

# Enhanced constraint propagation with optimizations
proc enhanced_propagate {} {
    variable domains
    variable constraints
    variable dependency_graph

    # Build dependency graph for efficient propagation
    build_dependency_graph

    # Use worklist algorithm for efficient propagation
    set worklist [dict keys $variables]
    set changed_vars [dict create]

    while {[llength $worklist] > 0} {
        set var [lindex $worklist 0]
        set worklist [lrange $worklist 1 end]

        foreach constraint [dict get $dependency_graph $var] {
            if {[process_constraint $constraint]} {
                # Add affected variables to worklist
                lassign $constraint A B min_delay max_delay
                if {$A == $var && ![dict exists $changed_vars $B]} {
                    lappend worklist $B
                    dict set changed_vars $B 1
                } elseif {$B == $var && ![dict exists $changed_vars $A]} {
                    lappend worklist $A
                    dict set changed_vars $A 1
                }
            }
        }

        dict unset changed_vars $var
    }
}