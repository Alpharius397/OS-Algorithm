class Heap{
    constructor() {
        this.size = 0;
        this.heap = new TreeNode(-1);
      }
    
    /**@param val number
     * @returns null
     * @description adds new value to heap
    */
    add(val){
        if(this.size==0){
            this.heap.val = val;
        }
        else{
            this.pushDown(this.heap,val);
        }

        this.size+=1;
    }

    /**@param null
     * @returns number | null
     * @description Pops minimum value from heap
    */
    pop(){
        
        var temp = this.heap.val;
        
        if(this.getSize()>0){
            this.popUp(this.heap);
        }
        else{
            temp = null;

            console.log("Empty Heap!");
        }

        this.size=Math.max(0,this.size-1);

        return temp;
    }

    /**@param null
     * @returns number
     * @description Returns size of heap
    */
    getSize(){
        return this.size;
    }

    /**@param root TreeNode
     * @returns bool
     * @description Helper function to check if tree has children
    */
    hasChild(root){
        return (root.left!=null || root.right!=null)
    }

    /**@param root TreeNode
     *@param val number 
     * @returns null
     * @description Helper function to pop values from heap
    */
    popUp(root,val){
        if(this.size<=1 || !this.hasChild(root)) return null;

        if(root.left==null){
            root.val = root.right.val;
            root.right = null;
        }
        else if(root.right==null){
            root.val = root.left.val;
            root.left = null;
        }
        else{
            var left = root.left.val, right = root.right.val;
            root.val = Math.min(left,right);        
            if(right<left){
                if(!this.hasChild(root.right)){
                    root.right=null;
                }
                else{
                    this.popUp(root.right,val);
                }
            }
            else{
                if(!this.hasChild(root.left)){
                    root.left=null;
                }
                else{
                    this.popUp(root.left,val);
                }
            }

    
        }
    }

    /**@param root TreeNode
     *@param val number 
     * @returns null
     * @description Helper function to push values into heap
    */
    pushDown(root,val){

        if(root.val<=val){

            if(root.left==null){
                root.left= new TreeNode(val);
            }
            else if(root.right==null){
                root.right = new TreeNode(val);
            }
            else{
                var left = root.left.val, right = root.right.val;

                if(right>left){
                    this.pushDown(root.right,val);
                }
                else{
                    this.pushDown(root.left,val);
                }
            }
        }
        else{
            
            if(root.left==null){
                root.left = new TreeNode(root.val)
            }
            else if(root.right==null){
                root.right = new TreeNode(root.val)
            }
            else{
                var left=root.left.val,right=root.right.val;

                if(right>left){
                    this.pushDown(root.right,root.val);
                }
                else{
                    this.pushDown(root.left,root.val);

                }
            }
            root.val = val;
        }

    }

    /**@param null 
     * @returns number[]
     * @description Returns an array representing the heap
    */
    getArray(){
        var stack_ = new Array();
        this.postOrder(this.heap,stack_)
        
        if(this.size>0) return stack_;
        return [];
    }

    /**@param root TreeNode
     *@param stack number[] 
     * @returns null
     * @description Helper function to get postorder of tree
    */
    postOrder(root,stack){

        stack.push(root.val);
        if(root.left!=null) this.postOrder(root.left,stack);
        if(root.right!=null) this.postOrder(root.right,stack);

    }

}

class TreeNode{
    constructor(_val) {
        this.val = _val;
        this.left=null;
        this.right=null;
      }

}

//var asd = new Heap();


