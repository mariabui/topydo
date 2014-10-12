from datetime import date

import AddCommand
import CommandTest
import TodoList

class AddCommandTest(CommandTest.CommandTest):
    def setUp(self):
        self.todolist = TodoList.TodoList([])
        self.today = date.today().isoformat()

    def test_add_task(self):
        args = ["New todo"]
        command = AddCommand.AddCommand(args, self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " New todo")
        self.assertEquals(self.errors, "")

    def test_add_multiple_args(self):
        args = ["New", "todo"]
        command = AddCommand.AddCommand(args, self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " New todo")
        self.assertEquals(self.errors, "")

    def test_add_priority1(self):
        command = AddCommand.AddCommand(["Foo (C)"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).priority(), 'C')
        self.assertEquals(self.todolist.todo(1).source(), "(C) " + self.today + " Foo")
        self.assertEquals(self.errors, "")

    def test_add_priority2(self):
        command = AddCommand.AddCommand(["Foo (CC)"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).priority(), None)
        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo (CC)")
        self.assertEquals(self.errors, "")

    def test_add_priority3(self):
        command = AddCommand.AddCommand(["Fo(C)o"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).priority(), None)
        self.assertEquals(self.todolist.todo(1).source(), self.today + " Fo(C)o" )
        self.assertEquals(self.errors, "")

    def test_add_priority4(self):
        command = AddCommand.AddCommand(["(C) Foo"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).priority(), 'C')
        self.assertEquals(self.todolist.todo(1).source(), "(C) " + self.today + " Foo")
        self.assertEquals(self.errors, "")

    def test_add_dep1(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out, self.err)
        command.execute()

        command = AddCommand.AddCommand(["Bar before:1"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo id:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar p:1")
        self.assertEquals(self.errors, "")

    def test_add_dep2(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out, self.err)
        command.execute()

        command = AddCommand.AddCommand(["Bar partof:1"], self.todolist)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo id:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar p:1")
        self.assertEquals(self.errors, "")

    def test_add_dep3(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist)
        command.execute()

        command = AddCommand.AddCommand(["Bar after:1"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo p:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar id:1")
        self.assertEquals(self.errors, "")

    def test_add_dep4(self):
        """ Test for using an after: tag with non-existing value. """
        command = AddCommand.AddCommand(["Foo after:1"], self.todolist, self.out, self.err)
        command.execute()

        self.assertFalse(self.todolist.todo(1).has_tag("after"))
        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo")
        self.assertEquals(self.output, "  1 " + str(self.todolist.todo(1)) + "\n")
        self.assertEquals(self.errors, "")

    def test_add_dep4(self):
        """ Test for using an after: tag with non-existing value. """
        command = AddCommand.AddCommand(["Foo after:2"], self.todolist, self.out, self.err)
        command.execute()

        self.assertFalse(self.todolist.todo(1).has_tag("after"))
        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo")
        self.assertEquals(self.output, "  1 " + str(self.todolist.todo(1)) + "\n")
        self.assertEquals(self.errors, "")

    def test_add_dep5(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out, self.err)
        command.execute()

        command = AddCommand.AddCommand(["Bar"], self.todolist, self.out, self.err)
        command.execute()

        command = AddCommand.AddCommand(["Baz before:1 before:2"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo id:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar id:2")
        self.assertEquals(self.todolist.todo(3).source(), self.today + " Baz p:1 p:2")
        self.assertEquals(self.errors, "")

    def test_add_dep6(self):
        command = AddCommand.AddCommand(["Foo"], self.todolist, self.out, self.err)
        command.execute()

        command = AddCommand.AddCommand(["Bar"], self.todolist, self.out, self.err)
        command.execute()

        command = AddCommand.AddCommand(["Baz after:1 after:2"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo p:1")
        self.assertEquals(self.todolist.todo(2).source(), self.today + " Bar p:1")
        self.assertEquals(self.todolist.todo(3).source(), self.today + " Baz id:1")
        self.assertEquals(self.errors, "")

    def test_add_reldate1(self):
        command = AddCommand.AddCommand(["Foo due:today"], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), self.today + " Foo due:" + self.today)
        self.assertEquals(self.errors, "")

    def test_add_reldate2(self):
        command = AddCommand.AddCommand(["Foo t:today due:today"], self.todolist, self.out, self.err)
        command.execute()

        result = "  1 %s Foo t:%s due:%s\n" % (self.today, self.today, self.today)
        self.assertEquals(self.output, result)
        self.assertEquals(self.errors, "")

    def test_add_empty(self):
        command = AddCommand.AddCommand([], self.todolist, self.out, self.err)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n")
