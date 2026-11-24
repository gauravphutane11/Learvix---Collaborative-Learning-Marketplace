"""Server-side SkillProof question bank. Correct answers never leave the server before submission."""
SKILL_BANK = {
"Python": [
("What is printed? x=[1,2,3]; y=x; y += [4]; print(x)", ["[1, 2, 3]", "[1, 2, 3, 4]", "[4]", "TypeError"], 1, "Both names reference the same list; += mutates it in place."),
("Which statement about a generator is correct?", ["It stores every yielded value", "It can be iterated only once and computes values lazily", "It is always faster than a list", "It supports random indexing"], 1, "Generators yield values lazily and their iteration state is consumed."),
("What is the output? print(bool([]), bool('0'), bool(0))", ["False False False", "False True False", "True True False", "False True True"], 1, "An empty list and numeric zero are false; a non-empty string is true."),
("Which key is valid for a dictionary? d={[1,2]: 'x'}", ["A list, because lists are ordered", "A tuple, because tuples are immutable", "A set, because sets are unique", "Any object"], 1, "Lists are unhashable; immutable tuples containing hashable values can be keys."),
("What does a context manager primarily guarantee?", ["A function runs asynchronously", "Resource setup and cleanup are coordinated", "Exceptions are always suppressed", "A block executes in a new process"], 1, "The context manager protocol calls __enter__ and __exit__, enabling reliable cleanup."),
("What is the average-case lookup complexity of a Python dict?", ["O(1)", "O(log n)", "O(n)", "O(n log n)"], 0, "Hash-table lookup is average O(1), with pathological worst cases possible."),
("What does nonlocal do inside a nested function?", ["Declares a module global", "Binds to a variable in the nearest enclosing function scope", "Makes a variable immutable", "Copies the variable"], 1, "nonlocal rebinds a name in an enclosing function scope."),
("Which is true about list.sort() and sorted(list)?", ["Both return a new list", "sort mutates and returns None; sorted returns a new list", "sorted mutates in place", "Neither supports a key function"], 1, "list.sort() is in-place; sorted() builds a new sorted list."),
("What is the output? a=[[]]*3; a[0].append(7); print(a)", ["[[7], [], []]", "[[7], [7], [7]]", "[[], [], []]", "Error"], 1, "The multiplication repeats references to the same inner list."),
("When can a finally block fail to execute?", ["When a function returns", "When an exception is raised", "When the process is forcibly terminated", "When a try block completes normally"], 2, "Abrupt process termination or a crash can prevent finally from running.")],
"JavaScript": [
("What is logged? console.log(typeof null)", ["null", "object", "undefined", "boolean"], 1, "This is a long-standing JavaScript language quirk."),
("What does Promise.all do when one input rejects?", ["Waits for every promise and returns partial values", "Rejects as soon as an input rejects", "Silently ignores the rejection", "Retries the failed promise"], 1, "Promise.all rejects on the first rejection; other operations are not cancelled."),
("What is the result of 0.1 + 0.2 === 0.3?", ["true", "false", "undefined", "TypeError"], 1, "Binary floating-point representation makes the sum slightly different from 0.3."),
("Which statement about const is correct?", ["The referenced object is deeply immutable", "The binding cannot be reassigned, but an object can still be mutated", "It is block-global", "It is hoisted without a temporal dead zone"], 1, "const prevents reassignment of the binding, not mutation of referenced objects."),
("What does Array.prototype.map return?", ["The original array, mutated", "A new array containing callback results", "An iterator", "A boolean"], 1, "map creates a new array and leaves the original array unchanged."),
("In an async function, what does await do with a rejected promise?", ["Returns the rejection object", "Throws the rejection reason at that point", "Converts it to null", "Blocks the browser thread"], 1, "A rejected promise causes await to throw, allowing try/catch handling."),
("What is the output? console.log('5' - 2, '5' + 2)", ["3 7", "52 7", "3 52", "NaN 52"], 2, "Subtraction coerces to number; + concatenates when a string is present."),
("What is a closure?", ["A function bundled with its lexical environment", "A function that has no parameters", "A class with private fields", "A promise callback"], 0, "A closure retains access to variables from its lexical scope."),
("Which event phase runs after capture and before bubbling?", ["Target phase", "Compile phase", "Microtask phase", "Render phase"], 0, "The event travels through capture, target, then bubble phases."),
("What does Object.freeze() do?", ["Deep-freezes nested objects", "Prevents extensions and makes own data properties non-writable/non-configurable", "Serializes the object", "Prevents reading properties"], 1, "Object.freeze is shallow; nested objects remain mutable unless frozen separately.")],
"SQL": [
("Which clause filters groups after aggregation?", ["WHERE", "HAVING", "ORDER BY", "LIMIT"], 1, "WHERE filters rows before grouping; HAVING filters aggregated groups."),
("What does COUNT(column) exclude?", ["Duplicate values", "NULL values", "Zero values", "Negative values"], 1, "COUNT(column) counts non-NULL values; COUNT(*) counts rows."),
("A LEFT JOIN returns which rows?", ["Only matching rows", "All left rows and matching right rows; unmatched right columns are NULL", "All right rows", "Only unmatched rows"], 1, "LEFT JOIN preserves every row from the left relation."),
("Which index is generally most useful for WHERE email = ?", ["A B-tree index on email", "An index on an unrelated timestamp", "A full-text index on every column", "No index can help equality"], 0, "A B-tree index commonly supports equality lookups and ordering."),
("What is a phantom read?", ["Reading uncommitted data", "Repeating a range query and seeing newly inserted/deleted matching rows", "Reading the same row twice", "A deadlock"], 1, "A concurrent transaction changes the set of rows matching a predicate."),
("Which constraint enforces uniqueness across a pair of columns?", ["CHECK on each column separately", "Composite UNIQUE constraint", "DEFAULT constraint", "NOT NULL only"], 1, "A composite unique constraint applies uniqueness to the column combination."),
("What does ROLLBACK do?", ["Permanently saves changes", "Reverts uncommitted changes in the current transaction", "Deletes the database", "Restarts the server"], 1, "ROLLBACK aborts the current transaction's uncommitted work."),
("Which query returns departments with more than 5 employees?", ["SELECT dept FROM staff WHERE COUNT(*)>5 GROUP BY dept", "SELECT dept FROM staff GROUP BY dept HAVING COUNT(*)>5", "SELECT dept FROM staff HAVING COUNT(*)>5", "SELECT dept FROM staff ORDER BY COUNT(*)>5"], 1, "Aggregate conditions belong in HAVING after GROUP BY."),
("What is the purpose of a foreign key?", ["Encrypt a column", "Enforce referential integrity between related tables", "Automatically index every query", "Guarantee row order"], 1, "Foreign keys constrain references to valid parent keys."),
("Which isolation level prevents dirty reads but may allow non-repeatable reads?", ["READ UNCOMMITTED", "READ COMMITTED", "SERIALIZABLE", "AUTOCOMMIT"], 1, "READ COMMITTED prevents dirty reads but permits changes between statements.")],
"React": [
("Why should state updates based on previous state use a functional updater?", ["It disables rendering", "It avoids stale state when updates are batched", "It mutates state safely", "It bypasses hooks"], 1, "The updater receives the latest queued state value."),
("What is the purpose of a key in a mapped list?", ["Style list items", "Help React identify item identity across renders", "Make elements accessible", "Prevent all rerenders"], 1, "Stable keys help reconciliation preserve the correct component identity."),
("When does useEffect cleanup run?", ["Only when the browser closes", "Before the effect reruns and on unmount", "Before every render", "Only after an error"], 1, "Cleanup runs before the next effect setup and when the component unmounts."),
("Why can an object dependency cause repeated effects?", ["Objects cannot be dependencies", "A new object reference is created on each render", "Effects compare JSON deeply", "React freezes dependencies"], 1, "Dependency comparison uses Object.is; new object references differ."),
("What does React.memo primarily optimize?", ["Network requests", "Rerendering when props are shallowly unchanged", "State persistence", "DOM event bubbling"], 1, "React.memo can skip a render when props compare equal."),
("Which is the correct controlled input pattern?", ["defaultValue only", "value paired with onChange updating state", "Read DOM value only on unmount", "Use innerHTML"], 1, "A controlled input receives its value from state and updates through onChange."),
("What problem does useContext solve?", ["All state management", "Passing values through a tree without manually threading props at every level", "Persisting state across reloads", "Making API calls"], 1, "Context provides values to descendants without prop drilling."),
("Why must hooks not be called conditionally?", ["Hooks are asynchronous", "React relies on the same hook call order on every render", "Conditional hooks are slower", "JSX forbids them"], 1, "Hook ordering maps each hook call to its stored state/effect slot."),
("What is a common cause of an infinite effect loop?", ["An effect has no dependencies and updates state", "An effect returns cleanup", "A component has a key", "Using a fragment"], 0, "An effect without dependencies runs after each render; a state update triggers another render."),
("When is useMemo appropriate?", ["For every variable", "To cache an expensive calculation when dependencies are unchanged", "To replace all useState calls", "To make a function asynchronous"], 1, "useMemo is a performance optimization, not a correctness requirement.")],
"UI/UX Design": [
("A checkout has high abandonment at the address step. What is the strongest first research action?", ["Change the brand colour", "Observe session recordings and usability-test the address flow", "Add more animations", "Increase the font size everywhere"], 1, "Investigate actual friction before choosing a design intervention."),
("Which metric best captures task efficiency in a usability test?", ["Total page views", "Time on task alongside task success and error rate", "Number of colours", "Social followers"], 1, "Efficiency is interpreted with effectiveness and errors, not in isolation."),
("What is the main risk of using colour alone for error states?", ["It increases bandwidth", "Users with colour-vision deficiencies may miss the distinction", "It prevents keyboard use", "It reduces contrast automatically"], 1, "Pair colour with text, icons or other non-colour cues."),
("A responsive layout breaks at intermediate widths. Which approach is most robust?", ["Design only for popular device models", "Use content-driven breakpoints and flexible layout constraints", "Set fixed pixel widths for all panels", "Hide all secondary content"], 1, "Breakpoints should respond to where content no longer fits."),
("What does a design system primarily provide?", ["A single landing page", "Reusable components, tokens and usage guidance for consistency", "A replacement for user research", "A guarantee of accessibility"], 1, "A design system aligns reusable patterns, foundations and documentation."),
("Which contrast target is generally recommended for normal text under WCAG AA?", ["2:1", "3:1", "4.5:1", "7:1 minimum in every case"], 2, "WCAG AA generally requires 4.5:1 for normal text; large text has a 3:1 threshold."),
("What is the best reason to use progressive disclosure?", ["Hide important controls", "Present essential choices first and reveal complexity when relevant", "Reduce all content to icons", "Avoid navigation"], 1, "Progressive disclosure manages complexity without removing access to advanced options."),
("A/B testing shows a 1% conversion lift but the sample is underpowered. What should the team do?", ["Ship immediately", "Continue or redesign the test to reach adequate statistical power", "Declare the variant a winner", "Ignore the control group"], 1, "An underpowered test cannot reliably distinguish signal from noise."),
("Which practice best supports keyboard accessibility?", ["Remove focus outlines", "Ensure logical tab order and visible focus indicators", "Use clickable divs without roles", "Trap focus on every page"], 1, "Keyboard users need predictable focus order and clear focus visibility."),
("A user repeatedly misses a primary action. What is the most evidence-based next step?", ["Make every button the same colour", "Review hierarchy, placement and task context with usability testing", "Add a tooltip and stop testing", "Increase animation speed"], 1, "Validate discoverability issues in context before choosing a solution.")]
}

def public_quiz(skill):
    questions = SKILL_BANK[skill]
    return [{"id": f"{i+1}", "question": q, "options": opts} for i, (q, opts, _answer, _why) in enumerate(questions)]

def grade_quiz(skill, answers):
    questions = SKILL_BANK[skill]
    details = []
    correct = 0
    for i, (question, options, answer, explanation) in enumerate(questions):
        selected = answers.get(str(i+1))
        is_correct = isinstance(selected, int) and selected == answer
        correct += int(is_correct)
        details.append({"id": str(i+1), "question": question, "selected": selected, "correctAnswer": answer, "correctOption": options[answer], "isCorrect": is_correct, "explanation": explanation})
    return correct, details
