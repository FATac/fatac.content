
<cfcomponent
	output="false"
	hint="I provide access to the photo tags.">
	
	
	<cffunction 
		name="init" 
		access="public" 
		returntype="any" 
		output="false" 
		hint="I initialize this component instance.">
	
		<!--- 
			For this demo, we are going simply going to cache the
			photo tag data in the variables scope; typically this 
			would come oud of a database, but we're keeping it 
			simple for the proof of concept.
			
			These tag items will have the following properties:
			- id
			- x
			- y
			- width
			- height
			- message
			- photoID
		--->
		<cfset variables.tags = [] />
			
		<!--- Return this object reference. --->
		<cfreturn this />
	</cffunction>
	
	
	<cffunction 
		name="deleteTag" 
		access="public" 
		returntype="any" 
		output="false" 
		hint="I delete the tag with the given ID.">
		
		<!--- Define arguments. --->	
		<cfargument 
			name="id" 
			type="string" 
			required="true" 
			hint="I am the ID (UUID) of the tag being deleted."
			/>
		
		<!--- Define the local scope. --->
		<cfset var local = {} />
		
		<!--- 
			We are going to be mutating the tag collection; as 
			such, let's put a lock around the array.
		--->
		<cflock
			name="tagMutation"
			type="exclusive"
			timeout="3">
		
			<!--- 
				Loop over the tags looking for the one to delete
				(the one with the matching ID). Since we are only
				deleting one, we can loop forward.
			--->
			<cfloop
				index="local.index"
				from="1"
				to="#arrayLen( variables.tags )#"
				step="1">
				
				<!--- Check to see if this ID matches. --->
				<cfif (variables.tags[ local.index ].id eq arguments.id)>
				
					<!--- This is the tag, delete it. --->
					<cfset arrayDeleteAt(
						variables.tags,
						local.index
						) />
				
					<!--- 
						Break out of the loop - we won't be 
						looking for any more items.
					--->
					<cfbreak />
				
				</cfif>
				
			</cfloop>
			
		</cflock>
		
		<!--- Return this object reference for chaining. --->
		<cfreturn this />
	</cffunction>
	
	
	<cffunction 
		name="getTagsByPhotoID" 
		access="public" 
		returntype="array" 
		output="false" 
		hint="I return the tag collection associated with the given ID.">
		
		<!--- Define arguments. --->
		<cfargument 
			name="photoID" 
			type="string" 
			required="true" 
			hint="I am the photo ID associated with the desired tag collection."
			/>
			
		<!--- Define the local scope. --->
		<cfset var local = {} />
		
		<!--- Create a tags collection. --->
		<cfset local.tags = [] />
		
		<!--- 
			Loop over the cached tags any copy any that have the 
			given photo ID. Because the array loop collection is 
			passed by VALUE, we don't need to lock this array.

			NOTE: This is based on the assumption that a tag's
			photoID can never change the tag's lifecycle - the
			only thing that would create a race condition.
		--->
		<cfloop
			index="local.tag"
			array="#variables.tags#">
			
			<!--- Check to see if this photo ID matches. --->
			<cfif (local.tag.photoID eq arguments.photoID)>
			
				<!--- 
					This tag is in the desired collection - add 
					it to our results.
				--->
				<cfset arrayAppend( local.tags, local.tag ) />
			
			</cfif>
			
		</cfloop>
		
		<!--- Return the tags. --->
		<cfreturn local.tags />		
	</cffunction>
	
	
	<cffunction 
		name="saveTag" 
		access="public" 
		returntype="string" 
		output="false" 
		hint="I save the given tag and return the new/existing tag ID.">
		
		<!--- Define arguments. --->	
		<cfargument 
			name="id" 
			type="string" 
			required="false" 
			default="" 
			hint="I am the ID (leave empty for new tags)."
			/>
		
		<cfargument 
			name="x" 
			type="numeric" 
			required="true" 
			hint="I am the x coordinate." 
			/>
			
		<cfargument 
			name="y" 
			type="numeric" 
			required="true" 
			hint="I am the x coordinate." 
			/>
			
		<cfargument 
			name="width" 
			type="numeric" 
			required="true" 
			hint="I am the width of the tag." 
			/>
			
		<cfargument 
			name="height" 
			type="numeric" 
			required="true" 
			hint="I am the height of the tag." 
			/>
			
		<cfargument 
			name="message" 
			type="string" 
			required="true" 
			hint="I am the message associated with the tag." 
			/>
			
		<cfargument 
			name="photoID" 
			type="string" 
			required="true" 
			hint="I am the ID of the photo with which this tag is associated." 
			/>
		
		<!--- Define the local scope. --->
		<cfset var local = {} />
		
		<!--- 
			We are going to be mutating the tag collection; as 
			such, let's put a lock around the array.
		--->
		<cflock
			name="tagMutation"
			type="exclusive"
			timeout="3">
	
			<!--- 
				We don't yet know if the tag with the given ID 
				exists; as such, we need to loop over the array 
				to search for it.
			--->
			<cfloop
				index="local.tag"
				array="#variables.tags#">
				
				<!--- Check to see if this ID matches. --->
				<cfif (local.tag.id eq arguments.id)>
				
					<!--- 
						We have an existing tag. Just update the
						tag object (which was passed by reference).
					--->
					<cfset local.tag.x = arguments.x />
					<cfset local.tag.y = arguments.y />
					<cfset local.tag.width = arguments.width />
					<cfset local.tag.height = arguments.height />
					<cfset local.tag.message = arguments.message />
				
					<!--- 
						Return out of the function as we won't be 
						doing anything further.
					--->
					<cfreturn arguments.id />
					
				</cfif>
				
			</cfloop>
			
			
			<!--- 
				If we made it this far, then the given tag was
				not found. As such, we will be creating a new 
				tag object. 
			--->
			<cfset local.tag = {
				id = createUUID(),
				x = arguments.x,
				y = arguments.y,
				width = arguments.width,
				height = arguments.height,
				message = arguments.message,
				photoID = arguments.photoID
				} />
	
			<!--- Store the tag. --->
			<cfset arrayAppend( variables.tags, local.tag ) />
			
			<!--- Return the new tag ID. --->
			<cfreturn local.tag.id />
	
		</cflock>		
	</cffunction>
	
</cfcomponent>