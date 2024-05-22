export default function AddTask() {
    return (
    <form className="flex flex-col gap-x-3 w-full justify-between  items-center">
        <input
        type="text"
        placeholder="Add Task here"
        minLength={3}
        maxLength={54}
        required
        name="add_task"
        className="w-full px-2 py-1 border border-gray-100 rounded-md"
        />
        <button className="px-2 py-1 mt-4 bg-teal-600 text-white rounded-md w-full">Save</button>
    </form>
    );
}
