#@author squ3D

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def backtracking_search(self):
        pass

    def backjumping_search(self):
        pass

    def forward_checking_search(self):
        pass

    def solve(self, method='backtracking'):
        if method == 'backtracking':
            return self.backtracking_search()
        elif method == 'backjumping':
            return self.backjumping_search()
        elif method == 'forward_checking':
            return self.forward_checking_search()
        else:
            raise ValueError(f"Unknown method '{method}'")

    def backtracking_search(self):
        return self._backtrack({})

    def _backtrack(self, assignment):
        if self._is_complete(assignment):
            return assignment

        var = self._select_unassigned_variable(assignment)
        for value in self._order_domain_values(var, assignment):
            if self._is_consistent(var, value, assignment):
                assignment[var] = value
                result = self._backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def _is_complete(self, assignment):
        return set(assignment.keys()) == set(self.variables)

    def _select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var

    def _order_domain_values(self, var, assignment):
        return self.domains[var]

    def _is_consistent(self, var, value, assignment):
        assignment[var] = value
        for constraint in self.constraints:
            if not constraint(assignment):
                del assignment[var]
                return False
        del assignment[var]
        return True

    ef backjumping_search(self):
        return self._backjump({}, None)

    def _backjump(self, assignment, last_failed_var):
        if self._is_complete(assignment):
            return assignment

        var = self._select_unassigned_variable(assignment)
        for value in self._order_domain_values(var, assignment):
            if self._is_consistent(var, value, assignment):
                assignment[var] = value
                result = self._backjump(assignment, None)
                if result is not None:
                    return result
                del assignment[var]
            else:
                if var != last_failed_var:
                    last_failed_var = var
                    conflict_vars = self._get_conflict_variables(var, assignment)
                    if not conflict_vars:
                        return None
                    for conf_var in conflict_vars:
                        if conf_var != var:
                            self._reduce_domain(conf_var, assignment)
                    result = self._backjump(assignment, var)
                    if result is not None:
                        return result
                    for conf_var in conflict_vars:
                        if conf_var != var:
                            self._restore_domain(conf_var, assignment)
        return None

    def _get_conflict_variables(self, var, assignment):
        conflict_vars = []
        for constraint in self.constraints:
            if var in constraint.__code__.co_varnames:
                constraint_vars = [arg for arg in constraint.__code__.co_varnames if arg != var]
                if not constraint(assignment, *constraint_vars):
                    conflict_vars += constraint_vars
        return set(conflict_vars)

    def _reduce_domain(self, var, assignment):
        old_domain = self.domains[var][:]
        for value in old_domain:
            assignment[var] = value
            if not self._is_consistent(var, value, assignment):
                self.domains[var].remove(value)
        del assignment[var]

    def _restore_domain(self, var, assignment):
        self.domains[var] = self.domains[var] + [value for value in self._order_domain_values(var, assignment)
                                                 if value not in self.domains[var]]

    def forward_checking_search(self):
        return self._forward_checking({}, {})

    def _forward_checking(self, assignment, domain):
        if self._is_complete(assignment):
            return assignment

        var = self._select_unassigned_variable(assignment)
        for value in self._order_domain_values(var, assignment):
            if self._is_consistent(var, value, assignment):
                assignment[var] = value
                reduced_domains = {}
                for constraint in self.constraints:
                    if var in constraint.__code__.co_varnames:
                        constraint_vars = [arg for arg in constraint.__code__.co_varnames if arg != var]
                        for conf_var in constraint_vars:
                            if conf_var not in reduced_domains:
                                reduced_domains[conf_var] = self.domains[conf_var][:]
                            for conf_value in self.domains[conf_var]:
                                assignment[conf_var] = conf_value
                                if not self._is_consistent(conf_var, conf_value, assignment):
                                    reduced_domains[conf_var].remove(conf_value)
                            if not reduced_domains[conf_var]:
                                del assignment[var]
                                return None
                            del assignment[conf_var]
                result = self._forward_checking(assignment, reduced_domains)
                if result is not None:
                    return result
                del assignment[var]
                for conf_var, conf_domain in reduced_domains.items():
                    self.domains[conf_var] = conf_domain
        return None
